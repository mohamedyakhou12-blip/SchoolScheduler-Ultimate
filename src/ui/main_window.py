# -*- coding: utf-8 -*-
import sys, os
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QStackedWidget, QFrame, QStatusBar, QMenuBar, QMenu, QMessageBox, QApplication)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QFont
from src.core.i18n import tr, set_language, get_language, is_rtl
from src.core.models import Institution, create_all_tables, seed_demo_data
from src.ui.styles import APP_STYLESHEET
from src.ui.widgets.sidebar import Sidebar
from src.ui.widgets.page_header import PageHeader
from src.ui.pages.dashboard import DashboardPage
from src.ui.pages.institution import InstitutionPage
from src.ui.pages.cycles import CyclesPage
from src.ui.pages.sections import SectionsPage
from src.ui.pages.subjects import SubjectsPage
from src.ui.pages.teachers import TeachersPage
from src.ui.pages.rooms import RoomsPage
from src.ui.pages.time_slots import TimeSlotsPage
from src.ui.pages.generate import GeneratePage
from src.ui.pages.view_schedule import ViewSchedulePage
from src.ui.pages.absences import AbsencesPage
from src.ui.pages.settings import SettingsPage
from src.ui.pages.help import HelpPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SchoolScheduler Ultimate v7.0")
        self.resize(1400, 900); self.setMinimumSize(1200, 700)
        QApplication.instance().setStyleSheet(APP_STYLESHEET)
        create_all_tables()
        self._build_ui(); self._build_menu(); self._build_status(); self._apply_layout_direction()
    def _build_ui(self):
        central = QWidget(); self.setCentralWidget(central)
        ml = QHBoxLayout(central); ml.setContentsMargins(0,0,0,0); ml.setSpacing(0)
        self.sidebar = Sidebar()
        self.sidebar.page_changed.connect(self._on_page_changed)
        self.sidebar.demo_requested.connect(self._on_load_demo)
        self.sidebar.language_changed.connect(self._on_language_changed)
        ml.addWidget(self.sidebar)
        self.stack = QStackedWidget(); self.stack.setObjectName("mainStack")
        self.pages = {"dashboard":DashboardPage(),"institution":InstitutionPage(),"cycles":CyclesPage(),
            "sections":SectionsPage(),"subjects":SubjectsPage(),"teachers":TeachersPage(),
            "rooms":RoomsPage(),"time_slots":TimeSlotsPage(),"generate":GeneratePage(),
            "view":ViewSchedulePage(),"absences":AbsencesPage(),"settings":SettingsPage(),"help":HelpPage()}
        for page in self.pages.values(): self.stack.addWidget(page)
        self.stack.setCurrentWidget(self.pages["dashboard"])
        ml.addWidget(self.stack, 1)
    def _build_menu(self):
        mb = self.menuBar()
        fm = mb.addMenu("ملف")
        lm = fm.addMenu("اللغة")
        for lang_name, lang_code in [("العربية","ar"),("Français","fr"),("English","en")]:
            a = QAction(lang_name, self); a.triggered.connect(lambda _,l=lang_code: self._change_lang(l)); lm.addAction(a)
        fm.addSeparator()
        ea = QAction("خروج", self); ea.triggered.connect(self.close); fm.addAction(ea)
        hm = mb.addMenu("مساعدة")
        aa = QAction("حول", self); aa.triggered.connect(self._about); hm.addAction(aa)
    def _build_status(self):
        self.status = QStatusBar(); self.setStatusBar(self.status)
        inst = Institution.load()
        self.status.showMessage(f"{tr('institution_name')}: {inst.name} | {tr('institution_year')}: {inst.year}")
    def _apply_layout_direction(self):
        QApplication.setLayoutDirection(Qt.LayoutDirection.RightToLeft if is_rtl() else Qt.LayoutDirection.LeftToRight)
    def _on_page_changed(self, key):
        if key in self.pages:
            self.stack.setCurrentWidget(self.pages[key])
            if hasattr(self.pages[key], "refresh"): self.pages[key].refresh()
    def _on_load_demo(self):
        r = QMessageBox.question(self, tr("confirm"), "تحميل بيانات تجريبية?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if r == QMessageBox.StandardButton.Yes:
            from src.core.database import db
            for t in ["schedule_entries","schedules","absences","locked_sessions","time_slots",
                "teacher_sections","rooms","teachers","subject_hours","subjects","sections","levels","cycles"]:
                db.execute(f"DELETE FROM {t};")
            db.execute("DELETE FROM sqlite_sequence;")
            if seed_demo_data():
                QMessageBox.information(self, tr("msg_saved"), tr("demo_loaded"))
                for p in self.pages.values():
                    if hasattr(p,"refresh"): p.refresh()
    def _on_language_changed(self, lang):
        self._change_lang(lang)
    def _change_lang(self, lang):
        set_language(lang); self._apply_layout_direction()
        QMessageBox.information(self, tr("language"), "أعد تشغيل البرنامج لتطبيق التغييرات بالكامل")
    def _about(self):
        QMessageBox.about(self, "حول", "<h3>SchoolScheduler Ultimate</h3><p>v7.0.0</p><p>Python + PyQt6 + SQLite</p>")
    def closeEvent(self, event):
        from src.core.database import db; db.close(); event.accept()
