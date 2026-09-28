# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QButtonGroup,
    QFrame, QScrollArea, QComboBox, QHBoxLayout, QSizePolicy)
from PyQt6.QtCore import Qt, pyqtSignal
from src.core.i18n import tr, get_language, is_rtl

class SidebarButton(QPushButton):
    def __init__(self, key, icon, label, parent=None):
        super().__init__(label, parent)
        self.key = key; self.setObjectName("navButton")
        self.setCheckable(True); self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setText(f"  {icon}  {label}")
        self.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.setMinimumHeight(44)

class Sidebar(QFrame):
    page_changed = pyqtSignal(str)
    demo_requested = pyqtSignal()
    language_changed = pyqtSignal(str)
    def __init__(self, parent=None):
        super().__init__(parent); self.setObjectName("Sidebar")
        self.setFixedWidth(260); self._build_ui()
    def _build_ui(self):
        layout = QVBoxLayout(self); layout.setContentsMargins(0,0,0,0); layout.setSpacing(0)
        title = QLabel("SchoolScheduler\nUltimate v7.0")
        title.setObjectName("sidebarTitle"); title.setWordWrap(True); layout.addWidget(title)
        layout.addWidget(self._sep())
        scroll = QScrollArea(); scroll.setWidgetResizable(True); scroll.setFrameShape(QFrame.Shape.NoFrame)
        container = QWidget(); cl = QVBoxLayout(container)
        cl.setContentsMargins(0,8,0,8); cl.setSpacing(2)
        self.btn_group = QButtonGroup(self); self.btn_group.setExclusive(True)
        nav = [("dashboard","📊","لوحة التحكم"),("institution","🏫","المؤسسة"),
            ("cycles","📚","الأطوار"),("sections","👨‍🎓","الأقسام"),
            ("subjects","📖","المواد"),("teachers","👨‍🏫","الأساتذة"),
            ("rooms","🚪","القاعات"),("time_slots","⏰","الأوقات"),
            ("generate","🤖","إنشاء الجدول"),("view","🔍","عرض الجداول"),
            ("absences","📅","الغيابات"),("settings","⚙️","الإعدادات"),("help","❓","المساعدة")]
        for key,icon,label in nav:
            btn = SidebarButton(key,icon,label)
            btn.clicked.connect(lambda _,k=key: self.page_changed.emit(k))
            self.btn_group.addButton(btn); cl.addWidget(btn)
        cl.addStretch()
        demo_btn = QPushButton("📦 تحميل بيانات تجريبية")
        demo_btn.setObjectName("navButtonPrimary"); demo_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        demo_btn.clicked.connect(self.demo_requested.emit); cl.addWidget(demo_btn)
        ll = QHBoxLayout(); self.lang_combo = QComboBox()
        self.lang_combo.addItem("العربية","ar"); self.lang_combo.addItem("Français","fr")
        self.lang_combo.addItem("English","en")
        cur = get_language()
        for i in range(self.lang_combo.count()):
            if self.lang_combo.itemData(i) == cur: self.lang_combo.setCurrentIndex(i); break
        self.lang_combo.currentIndexChanged.connect(lambda i: self.language_changed.emit(self.lang_combo.itemData(i)))
        ll.addWidget(QLabel("🌐")); ll.addWidget(self.lang_combo,1); cl.addLayout(ll)
        scroll.setWidget(container); layout.addWidget(scroll,1)
        if self.btn_group.buttons(): self.btn_group.buttons()[0].setChecked(True)
    def _sep(self):
        s = QFrame(); s.setFrameShape(QFrame.Shape.HLine)
        s.setStyleSheet("background-color: #334155; max-height: 1px;"); return s
