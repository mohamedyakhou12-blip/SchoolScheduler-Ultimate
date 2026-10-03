# -*- coding: utf-8 -*-
"""نظام إدارة الجداول المدرسية v7.0 - نقطة التشغيل"""
import sys, os, traceback

if getattr(sys, 'frozen', False):
    SCRIPT_DIR = os.path.dirname(sys.executable)
    base_dir = sys._MEIPASS if hasattr(sys, '_MEIPASS') else SCRIPT_DIR
    sys.path.insert(0, base_dir)
else:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, SCRIPT_DIR)

def setup_environment():
    os.makedirs(os.path.join(SCRIPT_DIR, "resources"), exist_ok=True)
    if sys.platform.startswith("linux") and not os.environ.get("DISPLAY"):
        os.environ["QT_QPA_PLATFORM"] = "offscreen"

def check_dependencies():
    if getattr(sys, 'frozen', False): return
    missing = []
    for mod in ["PyQt5", "reportlab", "openpyxl"]:
        try: __import__(mod)
        except ImportError: missing.append(mod)
    if missing:
        print(f"⚠️ pip install {' '.join(missing)}")
        sys.exit(1)

def run_app():
    setup_environment()
    check_dependencies()
    try:
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtGui import QFont, QIcon
        from src.core.i18n import tr, set_language
        from src.core.models import Institution, create_all_tables
        from src.ui.main_window import MainWindow
        from src.ui.styles import APP_STYLESHEET
        create_all_tables()
        inst = Institution.load()
        set_language(inst.language or "ar")
        app = QApplication(sys.argv)
        app.setApplicationName("SchoolScheduler Ultimate")
        app.setApplicationVersion("7.0.0")
        app.setStyleSheet(APP_STYLESHEET)
        icon_path = os.path.join(SCRIPT_DIR, "resources", "icon.ico")
        if os.path.exists(icon_path):
            app.setWindowIcon(QIcon(icon_path))
        font = QFont()
        for fname in ["Noto Sans Arabic", "Cairo", "Tahoma", "DejaVu Sans", "Arial", "Segoe UI"]:
            try:
                from PyQt5.QtGui import QFontDatabase
                if fname in set(QFontDatabase.families()):
                    font.setFamily(fname); break
            except: pass
        font.setPointSize(10)
        app.setFont(font)
        window = MainWindow()
        window.show()
        return app.exec()
    except Exception as e:
        traceback.print_exc()
        print(f"\n❌ {e}")
        return 1

if __name__ == "__main__":
    sys.exit(run_app())
