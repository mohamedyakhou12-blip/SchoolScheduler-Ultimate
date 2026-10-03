# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit, QLabel,
    QCheckBox, QComboBox, QFrame, QPushButton, QMessageBox, QScrollArea)
from PyQt5.QtCore import Qt
from src.core.i18n import tr, set_language, get_language
from src.core.models import Institution
from src.ui.widgets.page_header import PageHeader

class InstitutionPage(QWidget):
    def __init__(self):
        super().__init__(); self.inst = Institution.load(); self._build_ui()
    def _build_ui(self):
        layout = QVBoxLayout(self); layout.setContentsMargins(0,0,0,0)
        layout.addWidget(PageHeader(tr("institution_title"), "إعدادات المؤسسة"))
        scroll = QScrollArea(); scroll.setWidgetResizable(True); scroll.setFrameShape(QFrame.NoFrame)
        content = QWidget(); cl = QVBoxLayout(content); cl.setContentsMargins(24,16,24,24)
        card = QFrame(); card.setObjectName("card"); cl2 = QVBoxLayout(card); cl2.setContentsMargins(24,20,24,20)
        title = QLabel(tr("institution_title")); title.setObjectName("cardTitle"); cl2.addWidget(title)
        form = QFormLayout(); form.setSpacing(12)
        self.name_edit = QLineEdit(self.inst.name); self.name_edit.setPlaceholderText(tr("institution_name"))
        form.addRow(tr("institution_name") + ":", self.name_edit)
        self.year_edit = QLineEdit(self.inst.year); form.addRow(tr("institution_year") + ":", self.year_edit)
        self.lang_combo = QComboBox()
        self.lang_combo.addItem("العربية","ar"); self.lang_combo.addItem("Français","fr"); self.lang_combo.addItem("English","en")
        for i in range(self.lang_combo.count()):
            if self.lang_combo.itemData(i) == self.inst.language: self.lang_combo.setCurrentIndex(i); break
        form.addRow(tr("language") + ":", self.lang_combo)
        cl2.addLayout(form)
        sep = QFrame(); sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("background-color: #334155; max-height: 1px; margin: 16px 0;"); cl2.addWidget(sep)
        self.fixed_rooms_check = QCheckBox(tr("use_fixed_rooms")); self.fixed_rooms_check.setChecked(self.inst.use_fixed_rooms); cl2.addWidget(self.fixed_rooms_check)
        self.distribute_check = QCheckBox(tr("distribute_subjects")); self.distribute_check.setChecked(self.inst.distribute_subjects); cl2.addWidget(self.distribute_check)
        self.respect_hours_check = QCheckBox(tr("respect_teacher_hours")); self.respect_hours_check.setChecked(self.inst.respect_teacher_hours); cl2.addWidget(self.respect_hours_check)
        save_btn = QPushButton("💾 " + tr("save")); save_btn.setObjectName("primaryButton")
        save_btn.setCursor(Qt.PointingHandCursor); save_btn.clicked.connect(self._save); cl2.addWidget(save_btn)
        cl.addWidget(card); cl.addStretch(); scroll.setWidget(content); layout.addWidget(scroll,1)
    def _save(self):
        self.inst.name = self.name_edit.text().strip() or "مدرستي"
        self.inst.year = self.year_edit.text().strip() or "2024-2025"
        self.inst.language = self.lang_combo.currentData()
        self.inst.use_fixed_rooms = self.fixed_rooms_check.isChecked()
        self.inst.distribute_subjects = self.distribute_check.isChecked()
        self.inst.respect_teacher_hours = self.respect_hours_check.isChecked()
        self.inst.save()
        if self.inst.language != get_language(): set_language(self.inst.language)
        QMessageBox.information(self, tr("msg_saved"), tr("msg_saved"))
    def refresh(self):
        self.inst = Institution.load()
        self.name_edit.setText(self.inst.name); self.year_edit.setText(self.inst.year)
        self.fixed_rooms_check.setChecked(self.inst.use_fixed_rooms)
        self.distribute_check.setChecked(self.inst.distribute_subjects)
        self.respect_hours_check.setChecked(self.inst.respect_teacher_hours)
