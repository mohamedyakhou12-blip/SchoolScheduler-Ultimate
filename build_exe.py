# -*- coding: utf-8 -*-
import os, sys, shutil, subprocess
from pathlib import Path
APP_NAME = "SchoolScheduler"
SCRIPT_DIR = Path(__file__).parent.absolute()
def build():
    cmd = [sys.executable, "-m", "PyInstaller", "--name", APP_NAME, "--noconfirm", "--clean",
        "--windowed", "--onefile",
        "--add-data", f"src/core/translations{os.pathsep}src/core/translations",
        "--add-data", f"resources{os.pathsep}resources",
        "--exclude-module", "tkinter", "--exclude-module", "matplotlib",
        "--exclude-module", "numpy", "--exclude-module", "pandas",
        "--exclude-module", "PyQt5", "--exclude-module", "PySide6"]
    icon = SCRIPT_DIR / "resources" / "icon.ico"
    if icon.exists(): cmd.extend(["--icon", str(icon)])
    cmd.append(str(SCRIPT_DIR / "main.py"))
    print("Building..."); subprocess.run(cmd, cwd=str(SCRIPT_DIR))
    exe = SCRIPT_DIR / "dist" / f"{APP_NAME}.exe"
    if not exe.exists(): exe = SCRIPT_DIR / "dist" / APP_NAME
    if exe.exists():
        size = exe.stat().st_size / (1024*1024)
        print(f"\n✓ {exe} ({size:.1f} MB)")
        app_dir = SCRIPT_DIR / "التطبيق"; app_dir.mkdir(exist_ok=True)
        shutil.copy2(exe, app_dir / exe.name)
        print(f"✓ Copied to {app_dir}")
    else: print("❌ Build failed")
if __name__ == "__main__": build()
