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
2. **Cryptographically Pinned:** Pinned to immutable Git tags/commits and SHA-256 hashes.
3. **Zero-Execution:** Installing a package *never* executes arbitrary build scripts or background daemons.

---

## 🚀 Using Packages in Aerix

### 1. Search for Verified Packages
```powershell
arx pkg search
arx pkg search json
```

### 2. Install a Verified Package
```powershell
arx pkg install AerixJson
```
This automatically runs the **Aerix Capability Security Scanner**, verifies the package against the registry, and installs clean `.arx` modules directly into `./modules/AerixJson`.

### 3. Import in your Code
```aerix
import AerixJson

fn main() {
    let data = AerixJson.parse("{\"status\":\"ok\"}")
    println(data)
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

## 🤝 Submitting Your Package

We welcome community packages! To add your library to this registry:

1. Fork this repository.
2. Add your package manifest under `packages/<YourPackageName>.json`.
3. Add an entry to `registry.json`.
4. Open a Pull Request. Our automated security bot and core team will review your code and merge it!
