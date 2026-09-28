# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt
from src.core.i18n import tr

class PageHeader(QWidget):
    def __init__(self, title, subtitle="", parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 16, 24, 8)
        layout.setSpacing(4)
        t = QLabel(title); t.setObjectName("pageTitle"); layout.addWidget(t)
        if subtitle:
            s = QLabel(subtitle); s.setObjectName("pageSubtitle"); layout.addWidget(s)
        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("background-color: #334155; max-height: 1px;")
        layout.addWidget(sep)
