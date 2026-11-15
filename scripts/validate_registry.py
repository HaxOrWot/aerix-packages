#!/usr/bin/env python3
"""
Aerix Community Package Registry Validator (CI/PR check)
Validates registry schema, ensures no unauthorized package deletions, and audits contributions.
"""

import sys
import json
import re
import subprocess
import os

REQUIRED_FIELDS = ["name", "version", "description", "repository", "risk_rating"]
NAME_REGEX = re.compile(r"^[A-Za-z0-9_\-]+$")
VERSION_REGEX = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+.*$")

def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    reg_path = os.path.join(repo_root, "registry.json")

    print("==================================================================")
    print("  AERIX PACKAGE REGISTRY VALIDATION")
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

    # Anti-Tampering Check: Check against base branch if running in Git
    try:
        # Check if git diff shows removed packages
        diff_cmd = ["git", "diff", "origin/main...HEAD", "--", "registry.json"]
        proc = subprocess.run(diff_cmd, cwd=repo_root, capture_output=True, text=True)
        if proc.returncode == 0 and proc.stdout:
            # Check for lines starting with '-' that remove package entries
            for line in proc.stdout.splitlines():
                if line.startswith("-") and not line.startswith("---"):
                    # Check if removing a package name
                    if '"name"' in line or '"repository"' in line:
                        errors.append(f"ANTI-TAMPER: PR attempts to delete or modify existing package entry: {line.strip()}")
    except Exception:
        pass

    if errors:
        print(f"\n❌ Validation FAILED with {len(errors)} error(s):")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)

    print(f"\n✅ Validation PASSED! {len(packages)} verified package(s) configured.")
    sys.exit(0)

if __name__ == "__main__":
    main()
