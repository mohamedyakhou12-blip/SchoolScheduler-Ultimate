# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QDialog, QFormLayout, QLineEdit, QComboBox,
    QMessageBox, QScrollArea)
from PyQt6.QtCore import Qt
from src.core.i18n import tr
from src.core.models import Section, Level, Room
from src.ui.widgets.page_header import PageHeader

class SectionDialog(QDialog):
    def __init__(self, parent=None, section=None, levels=None, rooms=None):
        super().__init__(parent)
        self.setWindowTitle(tr("add") if not section else tr("edit")); self.setMinimumWidth(400)
        l = QVBoxLayout(self); f = QFormLayout()
        self.level_combo = QComboBox()
        for lv in (levels or []): self.level_combo.addItem(f"{lv.cycle_name} → {lv.name}", lv.id)
        if section:
            for i in range(self.level_combo.count()):
                if self.level_combo.itemData(i) == section.level_id: self.level_combo.setCurrentIndex(i); break
        f.addRow("المستوى:", self.level_combo)
        self.name_edit = QLineEdit(section.name if section else ""); f.addRow("الاسم:", self.name_edit)
        self.room_combo = QComboBox(); self.room_combo.addItem("بدون قاعة ثابتة", None)
        for r in (rooms or []): self.room_combo.addItem(r.name, r.id)
        if section and section.fixed_room_id:
            for i in range(self.room_combo.count()):
                if self.room_combo.itemData(i) == section.fixed_room_id: self.room_combo.setCurrentIndex(i); break
        f.addRow("القاعة الثابتة:", self.room_combo); l.addLayout(f)
        b = QHBoxLayout()
        ok = QPushButton(tr("save")); ok.setObjectName("primaryButton"); ok.clicked.connect(self.accept)
        cancel = QPushButton(tr("cancel")); cancel.clicked.connect(self.reject)
        b.addWidget(ok); b.addWidget(cancel); l.addLayout(b)
    def get_data(self): return self.level_combo.currentData(), self.name_edit.text().strip(), self.room_combo.currentData()

class SectionsPage(QWidget):
    def __init__(self):
        super().__init__(); self._build_ui()
    def _build_ui(self):
        layout = QVBoxLayout(self); layout.setContentsMargins(0,0,0,0)
        layout.addWidget(PageHeader(tr("nav_sections"), tr("nav_sections")))
        scroll = QScrollArea(); scroll.setWidgetResizable(True); scroll.setFrameShape(QFrame.Shape.NoFrame)
        content = QWidget(); cl = QVBoxLayout(content); cl.setContentsMargins(24,16,24,24)
        card = QFrame(); card.setObjectName("card"); cl2 = QVBoxLayout(card); cl2.setContentsMargins(20,16,20,16)
        title = QLabel("👨‍🎓 " + tr("nav_sections")); title.setObjectName("cardTitle"); cl2.addWidget(title)
        btns = QHBoxLayout()
        ab = QPushButton("➕ إضافة"); ab.setObjectName("primaryButton"); ab.clicked.connect(self._add); btns.addWidget(ab)
        eb = QPushButton("✏️ تعديل"); eb.clicked.connect(self._edit); btns.addWidget(eb)
        db = QPushButton("🗑️ حذف"); db.setObjectName("dangerButton"); db.clicked.connect(self._delete); btns.addWidget(db)
        cl2.addLayout(btns)
        self.table = QTableWidget(); self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID","الاسم","المستوى","القاعة"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.table.setColumnWidth(0,60); self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers); cl2.addWidget(self.table)
        cl.addWidget(card); cl.addStretch(); scroll.setWidget(content); layout.addWidget(scroll,1); self._load()
    def _load(self):
        sections = Section.all(); rooms = {r.id: r.name for r in Room.all()}
        self.table.setRowCount(len(sections))
        for i,s in enumerate(sections):
            self.table.setItem(i,0,QTableWidgetItem(str(s.id))); self.table.setItem(i,1,QTableWidgetItem(s.name))
            self.table.setItem(i,2,QTableWidgetItem(f"{s.cycle_name} - {s.level_name}"))
            room_name = rooms.get(s.fixed_room_id,"—") if s.fixed_room_id else "—"
            self.table.setItem(i,3,QTableWidgetItem(room_name))
    def _sel_id(self):
        r=self.table.currentRow()
        return int(self.table.item(r,0).text()) if r>=0 and self.table.item(r,0) else None
    def _add(self):
        levels=Level.all()
        if not levels: QMessageBox.warning(self,"","أضف مستوى أولًا"); return
        d=SectionDialog(self,levels=levels,rooms=Room.all())
        if d.exec()==QDialog.DialogCode.Accepted:
            lid,name,rid=d.get_data()
            if name: Section(level_id=lid,name=name,fixed_room_id=rid).save(); self._load()
    def _edit(self):
        sid=self._sel_id()
        if not sid: return
        sections=Section.all(); sec=next((s for s in sections if s.id==sid),None)
        if sec:
            d=SectionDialog(self,sec,Level.all(),Room.all())
            if d.exec()==QDialog.DialogCode.Accepted:
                sec.level_id,sec.name,sec.fixed_room_id=d.get_data(); sec.save(); self._load()
    def _delete(self):
        sid=self._sel_id()
        if not sid: return
        if QMessageBox.question(self,tr("confirm"),tr("msg_confirm_delete"))==QMessageBox.StandardButton.Yes:
            sections=Section.all(); sec=next((s for s in sections if s.id==sid),None)
            if sec: sec.delete(); self._load()
    def refresh(self): self._load()
