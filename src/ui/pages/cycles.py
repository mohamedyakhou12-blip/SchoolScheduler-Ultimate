# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QDialog, QFormLayout, QLineEdit, QComboBox,
    QMessageBox, QScrollArea, QSplitter)
from PyQt6.QtCore import Qt
from src.core.i18n import tr
from src.core.models import Cycle, Level
from src.ui.widgets.page_header import PageHeader

class CycleDialog(QDialog):
    def __init__(self, parent=None, cycle=None):
        super().__init__(parent)
        self.setWindowTitle(tr("add") if not cycle else tr("edit")); self.setMinimumWidth(350)
        l = QVBoxLayout(self); f = QFormLayout()
        self.name_edit = QLineEdit(cycle.name if cycle else ""); f.addRow("الاسم:", self.name_edit); l.addLayout(f)
        b = QHBoxLayout()
        ok = QPushButton(tr("save")); ok.setObjectName("primaryButton"); ok.clicked.connect(self.accept)
        cancel = QPushButton(tr("cancel")); cancel.clicked.connect(self.reject)
        b.addWidget(ok); b.addWidget(cancel); l.addLayout(b)
    def get_name(self): return self.name_edit.text().strip()

class LevelDialog(QDialog):
    def __init__(self, parent=None, level=None, cycles=None):
        super().__init__(parent)
        self.setWindowTitle(tr("add") if not level else tr("edit")); self.setMinimumWidth(350)
        l = QVBoxLayout(self); f = QFormLayout()
        self.cycle_combo = QComboBox()
        for c in (cycles or []): self.cycle_combo.addItem(c.name, c.id)
        if level:
            for i in range(self.cycle_combo.count()):
                if self.cycle_combo.itemData(i) == level.cycle_id: self.cycle_combo.setCurrentIndex(i); break
        f.addRow("الطور:", self.cycle_combo)
        self.name_edit = QLineEdit(level.name if level else ""); f.addRow("الاسم:", self.name_edit); l.addLayout(f)
        b = QHBoxLayout()
        ok = QPushButton(tr("save")); ok.setObjectName("primaryButton"); ok.clicked.connect(self.accept)
        cancel = QPushButton(tr("cancel")); cancel.clicked.connect(self.reject)
        b.addWidget(ok); b.addWidget(cancel); l.addLayout(b)
    def get_data(self): return self.cycle_combo.currentData(), self.name_edit.text().strip()

class CyclesPage(QWidget):
    def __init__(self):
        super().__init__(); self._build_ui()
    def _build_ui(self):
        layout = QVBoxLayout(self); layout.setContentsMargins(0,0,0,0)
        layout.addWidget(PageHeader(tr("nav_cycles"), "الأطوار والمستويات"))
        scroll = QScrollArea(); scroll.setWidgetResizable(True); scroll.setFrameShape(QFrame.Shape.NoFrame)
        content = QWidget(); cl = QVBoxLayout(content); cl.setContentsMargins(24,16,24,24)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        # الأطوار
        lc = QFrame(); lc.setObjectName("card"); ll = QVBoxLayout(lc); ll.setContentsMargins(20,16,20,16)
        lt = QLabel("📚 الأطوار"); lt.setObjectName("cardTitle"); ll.addWidget(lt)
        bl = QHBoxLayout()
        ab = QPushButton("➕ إضافة"); ab.setObjectName("primaryButton"); ab.clicked.connect(self._add_cycle); bl.addWidget(ab)
        eb = QPushButton("✏️ تعديل"); eb.clicked.connect(self._edit_cycle); bl.addWidget(eb)
        db = QPushButton("🗑️ حذف"); db.setObjectName("dangerButton"); db.clicked.connect(self._del_cycle); bl.addWidget(db)
        ll.addLayout(bl)
        self.cycles_table = QTableWidget(); self.cycles_table.setColumnCount(2)
        self.cycles_table.setHorizontalHeaderLabels(["ID","الاسم"])
        self.cycles_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.cycles_table.setColumnWidth(0,60); self.cycles_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.cycles_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers); ll.addWidget(self.cycles_table)
        self.cur_cycle_label = QLabel(""); self.cur_cycle_label.setStyleSheet("color:#94A3B8;font-size:12px;"); ll.addWidget(self.cur_cycle_label)
        splitter.addWidget(lc)
        # المستويات
        rc = QFrame(); rc.setObjectName("card"); rl = QVBoxLayout(rc); rl.setContentsMargins(20,16,20,16)
        rt = QLabel("📊 المستويات"); rt.setObjectName("cardTitle"); rl.addWidget(rt)
        bl2 = QHBoxLayout()
        self.ab2 = QPushButton("➕ إضافة"); self.ab2.setObjectName("primaryButton"); self.ab2.clicked.connect(self._add_level); bl2.addWidget(self.ab2)
        eb2 = QPushButton("✏️ تعديل"); eb2.clicked.connect(self._edit_level); bl2.addWidget(eb2)
        db2 = QPushButton("🗑️ حذف"); db2.setObjectName("dangerButton"); db2.clicked.connect(self._del_level); bl2.addWidget(db2)
        rl.addLayout(bl2)
        self.levels_table = QTableWidget(); self.levels_table.setColumnCount(2)
        self.levels_table.setHorizontalHeaderLabels(["ID","الاسم"])
        self.levels_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.levels_table.setColumnWidth(0,60); self.levels_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.levels_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers); rl.addWidget(self.levels_table)
        splitter.addWidget(rc); splitter.setSizes([500,500])
        cl.addWidget(splitter); cl.addStretch(); scroll.setWidget(content); layout.addWidget(scroll,1)
        self.cycles_table.cellClicked.connect(self._on_cycle_selected); self._load_cycles()
    def _load_cycles(self):
        cycles = Cycle.all(); self.cycles_table.setRowCount(len(cycles))
        for i,c in enumerate(cycles):
            self.cycles_table.setItem(i,0,QTableWidgetItem(str(c.id))); self.cycles_table.setItem(i,1,QTableWidgetItem(c.name))
    def _on_cycle_selected(self, row, col):
        if row < 0: return
        cid = int(self.cycles_table.item(row,0).text()); c = Cycle.get(cid)
        if c: self.cur_cycle_label.setText(f"الطور: {c.name}"); self._load_levels(cid)
    def _load_levels(self, cid):
        levels = Level.by_cycle(cid); self.levels_table.setRowCount(len(levels))
        for i,l in enumerate(levels):
            self.levels_table.setItem(i,0,QTableWidgetItem(str(l.id))); self.levels_table.setItem(i,1,QTableWidgetItem(l.name))
    def _sel_cycle(self): 
        r=self.cycles_table.currentRow(); return int(self.cycles_table.item(r,0).text()) if r>=0 and self.cycles_table.item(r,0) else None
    def _sel_level(self):
        r=self.levels_table.currentRow(); return int(self.levels_table.item(r,0).text()) if r>=0 and self.levels_table.item(r,0) else None
    def _add_cycle(self):
        d=CycleDialog(self)
        if d.exec()==QDialog.DialogCode.Accepted and d.get_name():
            Cycle(name=d.get_name()).save(); self._load_cycles()
    def _edit_cycle(self):
        cid=self._sel_cycle()
        if not cid: return
        c=Cycle.get(cid); d=CycleDialog(self,c)
        if d.exec()==QDialog.DialogCode.Accepted and d.get_name(): c.name=d.get_name(); c.save(); self._load_cycles()
    def _del_cycle(self):
        cid=self._sel_cycle()
        if not cid: return
        if QMessageBox.question(self,tr("confirm"),tr("msg_confirm_delete"))==QMessageBox.StandardButton.Yes:
            Cycle(id=cid).delete(); self._load_cycles(); self.levels_table.setRowCount(0)
    def _add_level(self):
        cycles=Cycle.all()
        if not cycles: QMessageBox.warning(self,"","أضف طورًا أولًا"); return
        d=LevelDialog(self,cycles=cycles)
        if d.exec()==QDialog.DialogCode.Accepted:
            cid,name=d.get_data()
            if name: Level(cycle_id=cid,name=name).save()
            if self._sel_cycle(): self._load_levels(self._sel_cycle())
    def _edit_level(self):
        lid=self._sel_level()
        if not lid: return
        levels=Level.all(); level=next((l for l in levels if l.id==lid),None)
        if level: 
            d=LevelDialog(self,level,Cycle.all())
            if d.exec()==QDialog.DialogCode.Accepted:
                level.cycle_id,level.name=d.get_data(); level.save()
                if self._sel_cycle(): self._load_levels(self._sel_cycle())
    def _del_level(self):
        lid=self._sel_level()
        if not lid: return
        if QMessageBox.question(self,tr("confirm"),tr("msg_confirm_delete"))==QMessageBox.StandardButton.Yes:
            levels=Level.all(); level=next((l for l in levels if l.id==lid),None)
            if level: level.delete(); 
            if self._sel_cycle(): self._load_levels(self._sel_cycle())
    def refresh(self): self._load_cycles()
