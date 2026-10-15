<div align="center">

**English** · [Русский](./README.ru.md)

# ⚡ System Deploy Hub

### One-click batch software installer for Windows powered by Winget and CustomTkinter.

Select the apps you need or pick a ready-made preset to deploy your entire Windows environment silently in minutes.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![Winget](https://img.shields.io/badge/Winget-Package_Manager-0078D4?style=flat-square&logo=windows&logoColor=white)
![UI](https://img.shields.io/badge/UI-CustomTkinter-3B8ED0?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-Windows_10%2F11-0078D6?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-E0A800?style=flat-square)

**Quick Start** · **Features** · **Build EXE** · **Project Structure**

</div>

---

## Features

* **🎨 App Icons & Live Statuses**: Each application features a custom color badge icon and a real-time status indicator (`📥` queued, `⏳` installing, `✅` installed, `⚠️` attention needed, `❌` error).
* **🌐 Bilingual Interface (EN / RU)**: Switch between English and Russian instantaneously via the header toggle (`RU | EN`) or the **⚙️ Settings** dialog, automatically persisted in `hub_settings.json`.
* **⚡ Ready-Made Presets & Search**: Apply curated bundles (**Basic PC**, **Gaming**, **Developer**) in one click or filter packages live by name or `Winget ID`.
* **💾 JSON Profile Export & Import**: Save your custom software selection to a `.json` file and load it on any other machine.
* **🛡️ Thread-Safe & UAC-Aware**: Runs Winget installations in a background worker thread without freezing the UI, detects Administrator privileges, and handles standard Winget exit codes cleanly.

---

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Launch the application (running as Administrator is recommended to avoid multiple UAC prompts):
   ```bash
   python system_deploy_hub.py
   ```

---

## Build EXE

### Option 1: One-Click Local Build on Windows
Run `build_exe.bat` or execute:
```bash
python build_exe.py
```
The builder script automatically generates `app_icon.ico`, bundles `CustomTkinter`, and compiles a standalone **`dist/SystemDeployHub.exe`** with an embedded Administrator UAC manifest (`--uac-admin`).

### Option 2: Automated GitHub Actions Build
This repository includes `.github/workflows/build_exe.yml`. Every push to `main` or `master` automatically compiles `SystemDeployHub.exe` on `windows-latest` and uploads it under **Actions → Artifacts**.

---

## Project Structure

* `system_deploy_hub.py` — main GUI application with dynamic badge icons, live statuses, and EN/RU settings
* `build_exe.py` — automated `.ico` generator and `PyInstaller` single-file `.exe` builder
* `build_exe.bat` — one-click Windows batch launcher for building `SystemDeployHub.exe`
* `requirements.txt` — Python dependencies (`customtkinter`, `Pillow`, `pyinstaller`)
* `README.md` / `README.ru.md` — English and Russian documentation with top language switcher
* `.github/workflows/build_exe.yml` — GitHub Actions workflow for cloud Windows `.exe` builds
