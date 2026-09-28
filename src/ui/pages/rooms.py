# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QDialog, QFormLayout, QLineEdit, QComboBox,
    QSpinBox, QMessageBox, QScrollArea, QColorDialog, QTextEdit, QCheckBox, QListWidget,
    QListWidgetItem, QFileDialog, QMenu)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QAction
from src.core.i18n import tr
from src.core.models import *
from src.ui.widgets.page_header import PageHeader

class RoomsPage(QWidget):
    def __init__(self):
        super().__init__(); self._build_ui()
    def _build_ui(self):
        layout = QVBoxLayout(self); layout.setContentsMargins(0,0,0,0)
        layout.addWidget(PageHeader(tr("nav_rooms"), tr("nav_rooms")))
        scroll = QScrollArea(); scroll.setWidgetResizable(True); scroll.setFrameShape(QFrame.Shape.NoFrame)
        content = QWidget(); cl = QVBoxLayout(content); cl.setContentsMargins(24,16,24,24)
        card = QFrame(); card.setObjectName("card"); cl2 = QVBoxLayout(card); cl2.setContentsMargins(20,16,20,16)
        title = QLabel(tr("nav_rooms")); title.setObjectName("cardTitle"); cl2.addWidget(title)
        btns = QHBoxLayout()
        ab = QPushButton("➕ إضافة"); ab.setObjectName("primaryButton"); ab.clicked.connect(self._add); btns.addWidget(ab)
        eb = QPushButton("✏️ تعديل"); eb.clicked.connect(self._edit); btns.addWidget(eb)
        db = QPushButton("🗑️ حذف"); db.setObjectName("dangerButton"); db.clicked.connect(self._delete); btns.addWidget(db)
        cl2.addLayout(btns)
        self.table = QTableWidget(); self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID","الاسم","ملاحظات"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.setColumnWidth(0,60); self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers); cl2.addWidget(self.table)
        cl.addWidget(card); cl.addStretch(); scroll.setWidget(content); layout.addWidget(scroll,1); self._load()
    def _load(self):
        items = []
        if "rooms" == "subjects": items = [(s.id,s.name,s.color) for s in Subject.all()]
        elif "rooms" == "teachers": items = [(t.id,t.full_name,t.subject_name) for t in Teacher.all()]
        elif "rooms" == "rooms": items = [(r.id,r.name,r.room_type) for r in Room.all()]
        elif "rooms" == "time_slots": items = [(s.id,f"{s.start_time}-{s.end_time}",s.period_type) for s in TimeSlot.all()]
        elif "rooms" == "absences": items = [(a.id,str(a.day),a.period_type) for a in Absence.all()]
        else: items = []
        self.table.setRowCount(len(items))
        for i,item in enumerate(items):
            for j,val in enumerate(item): self.table.setItem(i,j,QTableWidgetItem(str(val)))
    def _add(self): pass
    def _edit(self): pass
    def _delete(self): pass
    def refresh(self): self._load()
