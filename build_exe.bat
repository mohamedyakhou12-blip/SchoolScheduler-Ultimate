@echo off
chcp 65001 >nul
cd /d "%~dp0"
python -m pip install --upgrade pip --quiet
python -m pip install -r requirements.txt --quiet
python -m pip install pyinstaller --quiet
python build_exe.py
pause
