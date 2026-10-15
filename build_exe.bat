@echo off
chcp 65001 >nul
title System Deploy Hub - EXE Builder
echo [1/2] Installing dependencies (customtkinter, pillow, pyinstaller)...
python -m pip install --upgrade pip customtkinter pillow pyinstaller
echo [2/2] Building SystemDeployHub.exe...
python build_exe.py
echo.
echo Done! Your executable is in dist\SystemDeployHub.exe
pause
