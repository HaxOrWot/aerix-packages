# Aerix Official Community Package Registry (`aerix-packages`)

<div align="center">

```text
       ___         _             ___          _                       
      / _ \___ ___(_)_ __  ___  / _ \___ ____| |_____ ____ ____ ___   
     / __ / -_) __/ /\ \ /|___|/ ___/ _ `/ __/  '_/ _ `/ _ `/ -_|_-<   
    /_/ |_\__/_/ /_//_\_\     /_/   \_,_/\__/_/\_\\_,_/\_, /\__/___/  
                                                      /___/           
```

### The Curated & Security-Verified Module Index for the Aerix Programming Language

[![Registry Status](https://img.shields.io/badge/registry-active-10B981.svg?style=flat-square)](#)
[![Audit Standard](https://img.shields.io/badge/security-capability%20audited-00DCFF.svg?style=flat-square)](#)
[![License](https://img.shields.io/badge/license-MIT%20%2F%20Apache--2.0-F59E0B.svg?style=flat-square)](#)

</div>

---

## 🌟 What is this Repository?

`aerix-packages` is the official, community-driven package registry for **Aerix**. Unlike unmoderated package registries that suffer from malware and supply-chain attacks, every package in this index is:

1. **Security-Audited:** Inspected for dangerous native Windows OS capabilities (e.g. process injection, memory tampering, keylogging hooks).
2. **Zero-Execution:** Installing a package *never* executes arbitrary build scripts or background daemons.
3. **Source-Native:** Packages compile directly into your application binary with zero garbage collection or runtime overhead.

---

## 🚀 Using Packages in Aerix

### 1. Search for Verified Packages
```powershell
arx pkg search
```

### 2. Install a Verified Package
```powershell
# By verified registry name:
arx pkg install <PackageName>

# Or directly by Git repository URL:
arx pkg install https://github.com/username/my-aerix-lib.git
```
This automatically runs the **Aerix Capability Security Scanner**, verifies the package against the registry, and installs clean `.arx` modules directly into `./modules/<PackageName>`.

### 3. Import in your Code
```aerix
import "modules/MyLib/mod.arx"

fn main() {
    // Call functions from your installed module!
}
```

---

## 🛡️ Security Audit Policy

Aerix automatically classifies all `#[extern]` bindings in every package:

| Risk Level | Native OS APIs | Action |
| :--- | :--- | :--- |
| **CLEAN / LOW** | Standard GUI (`user32.dll`), 2D Canvas (`gdi32.dll`), File I/O (`kernel32.dll`), Clocks | Permitted & Verified |
| **MODERATE** | Raw Network Sockets (`ws2_32.dll`), Registry Access (`advapi32.dll`) | Permitted with Prompt |
| **HIGH** | Process Spawning (`CreateProcess`), Keylogger Hooks (`SetWindowsHookEx`) | Restricted |
| **CRITICAL** | Memory Injection (`WriteProcessMemory`, `CreateRemoteThread`, `VirtualAllocEx`) | **BLOCKED by default** |

---

## 🤝 Submitting Your Package: Step-by-Step

Anyone can submit an Aerix package to this official index! Here is the complete walkthrough:

### Step 1: Create Your Package Repository
Create a Git repository on GitHub (e.g. `https://github.com/your-username/FastMath`).

In your repository, include:
* An **`aerix.json`** manifest:
  ```json
  {
    "name": "FastMath",
    "version": "1.0.0",
    "description": "High-performance mathematical utilities for Aerix",
    "author": "your-username",
    "license": "MIT",
    "main": "mod.arx"
  }
  ```
* Your `.arx` source files (e.g. `mod.arx`).
* A `README.md` documenting your functions.

### Step 2: Audit Your Code Locally
Ensure your code passes the Aerix security scanner:
```powershell
arx pkg audit .
```

### Step 3: Fork & Add Your Package
1. **Fork** this repository (`HaxOrWot/aerix-packages`).
2. Open `registry.json` in your fork and add your package entry to the `"packages"` array:
   ```json
   {
     "name": "FastMath",
     "version": "1.0.0",
     "description": "High-performance mathematical utilities for Aerix",
     "repository": "https://github.com/your-username/FastMath.git",
     "license": "MIT",
     "risk_rating": "CLEAN (LOW)",
     "capabilities": ["Pure Computation"],
     "tags": ["math", "utilities"]
   }
   ```
3. Test your contribution locally:
   ```powershell
   python scripts/validate_registry.py
   ```

### Step 4: Open a Pull Request
Submit a Pull Request (PR) from your fork to `HaxOrWot/aerix-packages:main`.

---

## 🔒 PR Safety & Anti-Tampering Protections

What happens when someone opens a Pull Request?

1. **Pull Requests do NOT modify the registry automatically:**
   * A PR is only a *proposal*. No files in this repository change until the repository maintainer reviews and clicks **"Merge"**.

2. **Automated CI Validation (`scripts/validate_registry.py`):**
   * **Anti-Deletion Guard:** If a PR attempts to delete existing packages or modify another author's repository URL, the automated CI check **fails immediately** with an error.
   * **Schema Verification:** Ensures valid SemVer, URL formats, and non-empty metadata.

3. **Maintainer Code Review:**
   * Maintainers review the visual diff on GitHub before merging. Invalid, malicious, or vandalized PRs are closed and discarded with a single click.
