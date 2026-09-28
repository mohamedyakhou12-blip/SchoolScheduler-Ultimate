# -*- coding: utf-8 -*-
import time
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QPushButton, QLineEdit, QProgressBar, QMessageBox, QScrollArea, QCheckBox, QTableWidget,
    QTableWidgetItem, QHeaderView)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from src.core.i18n import tr
from src.core.models import Schedule, ScheduleEntry, Institution
from src.core.engine import SchedulingEngine, SchedulingConfig
from src.ui.widgets.page_header import PageHeader

class ScheduleWorker(QThread):
    finished = pyqtSignal(object); error = pyqtSignal(str)
    def __init__(self, name, config):
        super().__init__(); self.name = name; self.config = config
    def run(self):
        try:
            engine = SchedulingEngine(self.config)
            self.finished.emit(engine.schedule(self.name))
        except Exception as e: self.error.emit(str(e))

class GeneratePage(QWidget):
    def __init__(self):
        super().__init__(); self.worker = None; self._build_ui()
    def _build_ui(self):
        layout = QVBoxLayout(self); layout.setContentsMargins(0,0,0,0)
        layout.addWidget(PageHeader(tr("generate_btn"), "إنشاء الجدول تلقائيًا"))
        scroll = QScrollArea(); scroll.setWidgetResizable(True); scroll.setFrameShape(QFrame.Shape.NoFrame)
        content = QWidget(); cl = QVBoxLayout(content); cl.setContentsMargins(24,16,24,24); cl.setSpacing(16)
        sc = QFrame(); sc.setObjectName("card"); sl = QVBoxLayout(sc); sl.setContentsMargins(24,20,24,20)
        t = QLabel("⚙️ إعدادات الجدولة"); t.setObjectName("cardTitle"); sl.addWidget(t)
        nf = QHBoxLayout()
        self.name_edit = QLineEdit(); self.name_edit.setText(f"جدول {time.strftime('%Y-%m-%d %H:%M')}")
        nf.addWidget(QLabel("الاسم:")); nf.addWidget(self.name_edit,1); sl.addLayout(nf)
        inst = Institution.load()
        ol = QHBoxLayout()
        self.fixed_check = QCheckBox(tr("use_fixed_rooms")); self.fixed_check.setChecked(inst.use_fixed_rooms); ol.addWidget(self.fixed_check)
        self.distribute_check = QCheckBox(tr("distribute_subjects")); self.distribute_check.setChecked(inst.distribute_subjects); ol.addWidget(self.distribute_check)
        self.respect_check = QCheckBox(tr("respect_teacher_hours")); self.respect_check.setChecked(inst.respect_teacher_hours); ol.addWidget(self.respect_check)
        sl.addLayout(ol)
        self.gen_btn = QPushButton(tr("generate_btn")); self.gen_btn.setObjectName("primaryButton")
        self.gen_btn.setMinimumHeight(50); self.gen_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.gen_btn.clicked.connect(self._generate); sl.addWidget(self.gen_btn)
        self.progress = QProgressBar(); self.progress.setVisible(False); self.progress.setRange(0,0); sl.addWidget(self.progress)
        cl.addWidget(sc)
        rc = QFrame(); rc.setObjectName("card"); rl = QVBoxLayout(rc); rl.setContentsMargins(24,20,24,20)
        rt = QLabel("📊 " + tr("schedule_metrics")); rt.setObjectName("cardTitle"); rl.addWidget(rt)
        self.result_label = QLabel("لا توجد نتائج بعد"); self.result_label.setStyleSheet("color: #94A3B8;"); rl.addWidget(self.result_label)
        cl.addWidget(rc)
        sv = QFrame(); sv.setObjectName("card"); svl = QVBoxLayout(sv); svl.setContentsMargins(24,20,24,20)
        svt = QLabel("📋 الجداول المحفوظة"); svt.setObjectName("cardTitle"); svl.addWidget(svt)
        self.saved_table = QTableWidget(); self.saved_table.setColumnCount(5)
        self.saved_table.setHorizontalHeaderLabels(["ID","الاسم","التاريخ","النقاط","التعارضات"])
        self.saved_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.saved_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.saved_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        svl.addWidget(self.saved_table)
        bl = QHBoxLayout()
        ab = QPushButton("✅ تفعيل"); ab.setObjectName("primaryButton"); ab.clicked.connect(self._activate); bl.addWidget(ab)
        db_btn = QPushButton("🗑️ حذف"); db_btn.setObjectName("dangerButton"); db_btn.clicked.connect(self._delete); bl.addWidget(db_btn)
        svl.addLayout(bl); cl.addWidget(sv); cl.addStretch()
        scroll.setWidget(content); layout.addWidget(scroll,1); self._load_schedules()
    def _generate(self):
        if self.worker and self.worker.isRunning(): return
        config = SchedulingConfig(use_fixed_rooms=self.fixed_check.isChecked(),
            distribute_subjects=self.distribute_check.isChecked(),
            respect_teacher_hours=self.respect_check.isChecked())
        self.gen_btn.setEnabled(False); self.progress.setVisible(True)
        self.result_label.setText("جارٍ إنشاء الجدول...")
        self.worker = ScheduleWorker(self.name_edit.text().strip() or "جدول", config)
        self.worker.finished.connect(self._on_finished); self.worker.error.connect(self._on_error)
        self.worker.start()
    def _on_finished(self, result):
        self.gen_btn.setEnabled(True); self.progress.setVisible(False)
        self.result_label.setText(f"📊 النتيجة:\n  • النجاح: {result.success}\n  • التعارضات: {result.conflicts_count}\n  • غير موزعة: {result.unassigned_count}\n  • النقاط: {result.score}/100\n  • الزمن: {result.execution_time:.2f} ثانية")
        if result.unassigned_tasks:
            self.result_label.setText(self.result_label.text() + "\n⚠️ تحذيرات:\n" + "\n".join(f"  • {w}" for w in result.unassigned_tasks[:10]))
        if result.success:
            r = QMessageBox.question(self, tr("confirm"), "تم! تفعيل الجدول?", QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No)
            if r == QMessageBox.StandardButton.Yes: Schedule.set_active(result.schedule_id)
        self._load_schedules()
    def _on_error(self, e):
        self.gen_btn.setEnabled(True); self.progress.setVisible(False)
        QMessageBox.critical(self, tr("msg_error"), str(e))
    def _load_schedules(self):
        schedules = Schedule.all(); self.saved_table.setRowCount(len(schedules))
        for i,s in enumerate(schedules):
            self.saved_table.setItem(i,0,QTableWidgetItem(str(s.id)))
            self.saved_table.setItem(i,1,QTableWidgetItem(s.name))
            self.saved_table.setItem(i,2,QTableWidgetItem(s.created_at))
            self.saved_table.setItem(i,3,QTableWidgetItem(f"{s.score}"))
            self.saved_table.setItem(i,4,QTableWidgetItem(str(s.conflicts_count)))
    def _activate(self):
        r = self.saved_table.currentRow()
        if r < 0: return
        sid = int(self.saved_table.item(r,0).text()); Schedule.set_active(sid)
        self._load_schedules(); QMessageBox.information(self, tr("msg_saved"), "تم التفعيل")
    def _delete(self):
        r = self.saved_table.currentRow()
        if r < 0: return
        sid = int(self.saved_table.item(r,0).text())
        if QMessageBox.question(self, tr("confirm"), tr("msg_confirm_delete")) == QMessageBox.StandardButton.Yes:
            ScheduleEntry.delete_schedule(sid); Schedule.get(sid).delete(); self._load_schedules()
    def refresh(self): self._load_schedules()
