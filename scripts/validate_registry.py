#!/usr/bin/env python3
"""
Aerix Community Package Registry Validator (CI/PR check)
Enforces:
1. JSON schema and SemVer compliance.
2. Anti-tampering (no deletions of existing packages).
3. Mandatory Project Structure:
   - Root: aerix.json, README.md, LICENSE
   - All .arx source files must live in src/
   - No .arx files outside src/
   - Non-code files (json, md, license) must be outside src/
"""

import sys
import json
import re
import subprocess
import os
import shutil
import tempfile

REQUIRED_FIELDS = ["name", "version", "description", "repository", "risk_rating"]
NAME_REGEX = re.compile(r"^[A-Za-z0-9_\-]+$")
VERSION_REGEX = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+.*$")

def validate_package_structure(pkg_name, repo_url):
    """Clones package into a temporary folder to verify mandatory project layout."""
    tmp_dir = tempfile.mkdtemp(prefix=f"aerix_val_{pkg_name}_")
    try:
        clone_cmd = ["git", "clone", "--depth", "1", repo_url, tmp_dir]
        proc = subprocess.run(clone_cmd, capture_output=True, text=True, timeout=30)
        if proc.returncode != 0:
            return [f"Failed to clone repository '{repo_url}': {proc.stderr.strip()}"]

        errors = []
        root_items = os.listdir(tmp_dir)

        # 1. aerix.json in root
        if "aerix.json" not in root_items:
            errors.append(f"Package '{pkg_name}' is missing mandatory 'aerix.json' in repository root.")
        else:
            try:
                with open(os.path.join(tmp_dir, "aerix.json"), "r", encoding="utf-8") as f:
                    manifest = json.load(f)
                main_file = manifest.get("main", "")
                if not main_file.startswith("src/"):
                    errors.append(f"Package '{pkg_name}': aerix.json 'main' must point to a file inside src/ (found: '{main_file}')")
            except Exception as e:
                errors.append(f"Package '{pkg_name}': Invalid aerix.json: {e}")

        # 2. README.md in root
        if not any(f.lower().startswith("readme") for f in root_items):
            errors.append(f"Package '{pkg_name}' is missing mandatory 'README.md' in repository root.")

        # 3. LICENSE in root
        if not any(f.lower().startswith("license") for f in root_items):
            errors.append(f"Package '{pkg_name}' is missing mandatory 'LICENSE' in repository root.")

        # 4. src/ folder is MANDATORY
        src_path = os.path.join(tmp_dir, "src")
        if not os.path.isdir(src_path):
            errors.append(f"Package '{pkg_name}' is missing mandatory 'src/' folder! All source code must be in src/.")
        else:
            # Check for at least one .arx file in src
            src_arx = []
            for root, _, files in os.walk(src_path):
                for f in files:
                    if f.endswith(".arx"):
                        src_arx.append(os.path.join(root, f))
                    elif f.endswith(".json") or f.endswith(".md"):
                        errors.append(f"Package '{pkg_name}': Non-code file '{f}' found inside src/. Documentation and JSON must live outside src/.")
            if not src_arx:
                errors.append(f"Package '{pkg_name}': No .arx source files found inside src/.")

        # 5. NO .arx files in root outside src/
        for item in root_items:
            if item.endswith(".arx"):
                errors.append(f"Package '{pkg_name}': Stray source file '{item}' found in root! All .arx files must live inside src/.")

        return errors
    except Exception as e:
        return [f"Package '{pkg_name}': Verification exception: {e}"]
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    reg_path = os.path.join(repo_root, "registry.json")

    print("==================================================================")
    print("  AERIX COMMUNITY PACKAGE REGISTRY VALIDATOR")
    print("==================================================================")
    print(f"Checking registry: {reg_path}")

    if not os.path.exists(reg_path):
        print("ERROR: registry.json not found!")
        sys.exit(1)

    try:
        with open(reg_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"ERROR: Failed to parse registry.json as valid JSON: {e}")
        sys.exit(1)

    if not isinstance(data, dict):
        print("ERROR: registry.json root must be a JSON object!")
        sys.exit(1)

    if "packages" not in data or not isinstance(data["packages"], list):
        print("ERROR: registry.json must contain a 'packages' array!")
        sys.exit(1)

    packages = data["packages"]
    seen_names = set()
    errors = []

    for idx, pkg in enumerate(packages):
        if not isinstance(pkg, dict):
            errors.append(f"Package #{idx} is not a JSON object")
            continue

        name = pkg.get("name", "")
        if not name or not NAME_REGEX.match(name):
            errors.append(f"Package #{idx} has invalid name '{name}'. Must be alphanumeric, underscores or hyphens.")
        
        name_lower = name.lower()
        if name_lower in seen_names:
            errors.append(f"Duplicate package name '{name}' found.")
        seen_names.add(name_lower)

        for field in REQUIRED_FIELDS:
            if field not in pkg or not str(pkg[field]).strip():
                errors.append(f"Package '{name}' is missing required field '{field}'")

        ver = str(pkg.get("version", ""))
        if not VERSION_REGEX.match(ver):
            errors.append(f"Package '{name}' has invalid SemVer version '{ver}' (expected X.Y.Z)")

        repo = str(pkg.get("repository", ""))
        if not (repo.startswith("https://") or repo.startswith("git@")):
            errors.append(f"Package '{name}' has invalid repository URL '{repo}' (must start with https:// or git@)")

    # Anti-Tampering Check: Check git diff against main
    try:
        diff_cmd = ["git", "diff", "origin/main...HEAD", "--", "registry.json"]
        proc = subprocess.run(diff_cmd, cwd=repo_root, capture_output=True, text=True)
        if proc.returncode == 0 and proc.stdout:
            for line in proc.stdout.splitlines():
                if line.startswith("-") and not line.startswith("---"):
                    if '"name"' in line or '"repository"' in line:
                        errors.append(f"ANTI-TAMPER: PR attempts to delete or modify existing package entry: {line.strip()}")
    except Exception:
        pass

    # Mandatory Structure Validation for each configured package
    print(f"\nAuditing mandatory project structure for {len(packages)} package(s)...")
    for pkg in packages:
        p_name = pkg.get("name")
        p_repo = pkg.get("repository")
        if p_name and p_repo:
            print(f"  Validating '{p_name}' ({p_repo})...")
            struct_errors = validate_package_structure(p_name, p_repo)
            errors.extend(struct_errors)

    if errors:
        print(f"\n❌ Validation FAILED with {len(errors)} error(s):")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)

    print(f"\n✅ Validation PASSED! All {len(packages)} packages satisfy the mandatory project layout.")
    sys.exit(0)

if __name__ == "__main__":
    main()
