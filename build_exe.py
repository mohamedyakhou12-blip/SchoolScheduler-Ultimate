# -*- coding: utf-8 -*-
import os, sys, shutil, subprocess
from pathlib import Path
APP_NAME = "SchoolScheduler"
SCRIPT_DIR = Path(__file__).parent.absolute()

def build():
    cmd = [sys.executable, "-m", "PyInstaller", "--name", APP_NAME, "--noconfirm", "--clean",
        "--windowed", "--onefile",
        "--add-data", f"src/core/translations{os.pathsep}src/core/translations"]
    
    resources_dir = SCRIPT_DIR / "resources"
    if resources_dir.exists() and any(resources_dir.iterdir()):
        cmd.extend(["--add-data", f"resources{os.pathsep}resources"])
    
    icon = resources_dir / "icon.ico"
    if icon.exists():
        cmd.extend(["--icon", str(icon)])
    
    for mod in ["tkinter", "matplotlib", "numpy", "pandas", "PyQt6", "PySide6", "PySide2"]:
        cmd.extend(["--exclude-module", mod])
    
    cmd.append(str(SCRIPT_DIR / "main.py"))
    
    print("Building...")
    result = subprocess.run(cmd, cwd=str(SCRIPT_DIR))
    
    if result.returncode != 0:
        print("❌ Build failed")
        return
    
    exe_path = SCRIPT_DIR / "dist" / f"{APP_NAME}.exe"
    if not exe_path.exists():
        exe_path = SCRIPT_DIR / "dist" / APP_NAME
    
    if exe_path.exists():
        size = exe_path.stat().st_size / (1024 * 1024)
        print(f"\n✓ Build successful!")
        print(f"  📍 Path: {exe_path}")
        print(f"  📦 Size: {size:.1f} MB")
        app_dir = SCRIPT_DIR / "التطبيق"
        app_dir.mkdir(exist_ok=True)
        shutil.copy2(exe_path, app_dir / exe_path.name)
        print(f"  📁 Copied to: {app_dir}")
        try:
            shutil.rmtree(SCRIPT_DIR / "build")
            os.remove(SCRIPT_DIR / f"{APP_NAME}.spec")
        except: pass
    else:
        print("❌ Build failed - exe not found")

if __name__ == "__main__":
    build()
