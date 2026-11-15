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

`aerix-packages` is the official community package registry for **Aerix**. It contains **only the metadata registry index (`registry.json`)** and CI validation scripts.

> [!IMPORTANT]
> **No package source code lives in this repository.** Every package is hosted in its own independent repository. The Aerix package manager (`arx pkg`) automatically clones the package from its Git repository and installs it into the local `./modules/<PackageName>` directory.

---

## 🚀 Using Packages in Aerix

### 1. List Available Packages
```powershell
arx pkg available
```

### 2. Search for a Package
```powershell
arx pkg search math
```

### 3. Install a Verified Package
```powershell
# By verified registry name:
arx pkg install VecMath

# Or directly by Git repository URL:
arx pkg install https://github.com/HaxOrWot/VecMath.git
```
This automatically runs the **Aerix Capability Security Scanner**, verifies the package against the registry, and installs clean `.arx` modules directly into `./modules/<PackageName>`.

---

## 📐 Mandatory Package Project Structure

Every package submitted to the registry **must** strictly conform to the following layout:

```text
<PackageName>/
├── aerix.json        <-- REQUIRED: Manifest in root (must point "main": "src/mod.arx")
├── README.md         <-- REQUIRED: Documentation and usage guide
├── LICENSE           <-- REQUIRED: Open-source license (MIT, Apache, etc.)
└── src/              <-- MANDATORY: ALL source files must be inside src/
    ├── mod.arx       <-- REQUIRED: Primary entry point
    └── ...           <-- Submodules, helper files, or subfolders
```

### Strict Rules Enforced by CI:
1. **Source Code Isolation**: All `.arx` files **must** live inside the `src/` directory. No loose `.arx` files are allowed in the repository root.
2. **Metadata Isolation**: `aerix.json`, `README.md`, `LICENSE`, and any non-code configuration files must live in the root directory **outside** `src/`.
3. **Primary Entry**: `aerix.json` must specify `"main": "src/mod.arx"`.
4. **Subdirectories Supported**: Packages can have multiple subfolders inside `src/` (e.g. `src/geom/rect.arx`); `arx` automatically discovers and links them recursively.

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

1. Create your package repository following the **Mandatory Layout** above.
2. Verify it passes the auditor locally:
   ```powershell
   arx pkg audit .
   ```
3. Fork `HaxOrWot/aerix-packages`.
4. In your fork, add an entry to `registry.json` under `"packages"`:
   ```json
   {
     "name": "YourPackageName",
     "version": "1.0.0",
     "description": "Short description of your package",
     "repository": "https://github.com/YourUsername/YourPackageName.git",
     "license": "MIT",
     "risk_rating": "CLEAN (LOW)"
   }
   ```
5. Test validation locally:
   ```powershell
   python scripts/validate_registry.py
   ```
6. Submit a **Pull Request (PR)**. Once reviewed, it will be merged and immediately available to all Aerix developers worldwide!
