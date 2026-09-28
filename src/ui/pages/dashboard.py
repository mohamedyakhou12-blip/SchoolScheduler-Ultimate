# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QGridLayout, QPushButton, QScrollArea, QSizePolicy)
from PyQt6.QtCore import Qt, pyqtSignal
from src.core.i18n import tr
from src.core.models import (Institution, Cycle, Level, Section, Subject, Teacher, Room, Schedule)
from src.ui.widgets.page_header import PageHeader

class StatCard(QFrame):
    def __init__(self, icon, label, value, color="#3B82F6"):
        super().__init__(); self.setObjectName("statCard")
        layout = QVBoxLayout(self); layout.setContentsMargins(20,16,20,16); layout.setSpacing(4)
        top = QHBoxLayout()
        il = QLabel(icon); il.setStyleSheet(f"font-size: 28px; color: {color};"); il.setAlignment(Qt.AlignmentFlag.AlignCenter)
        nl = QLabel(value); nl.setStyleSheet(f"color: {color}; font-size: 32px; font-weight: bold;")
        top.addWidget(il); top.addWidget(nl,1,Qt.AlignmentFlag.AlignLeft); layout.addLayout(top)
        ll = QLabel(label); ll.setStyleSheet("color: #94A3B8; font-size: 12px;"); layout.addWidget(ll)

class DashboardPage(QWidget):
    navigate_to = pyqtSignal(str)
    def __init__(self):
        super().__init__(); self._build_ui()
    def _build_ui(self):
        layout = QVBoxLayout(self); layout.setContentsMargins(0,0,0,0)
        layout.addWidget(PageHeader(tr("nav_dashboard"), tr("app_subtitle")))
        scroll = QScrollArea(); scroll.setWidgetResizable(True); scroll.setFrameShape(QFrame.Shape.NoFrame)
        content = QWidget(); cl = QVBoxLayout(content); cl.setContentsMargins(24,16,24,24); cl.setSpacing(16)
        inst = Institution.load()
        stats = [("🏫",tr("institution_title"),inst.name,"#3B82F6"),
            ("📚",tr("nav_cycles"),str(len(Cycle.all())),"#10B981"),
            ("📊","المستويات",str(len(Level.all())),"#F59E0B"),
            ("👨‍🎓",tr("nav_sections"),str(len(Section.all())),"#EF4444"),
            ("📖",tr("nav_subjects"),str(len(Subject.all())),"#06B6D4"),
            ("👨‍🏫",tr("nav_teachers"),str(len(Teacher.all())),"#8B5CF6"),
            ("🚪",tr("nav_rooms"),str(len(Room.all())),"#F97316")]
        sl = QGridLayout(); sl.setSpacing(12)
        for i,(icon,label,value,color) in enumerate(stats):
            sl.addWidget(StatCard(icon,label,value,color), i//4, i%4)
        cl.addLayout(sl)
        schedules = Schedule.all()
        active = next((s for s in schedules if s.is_active), None)
        if active:
            ac = QFrame(); ac.setObjectName("card"); al = QVBoxLayout(ac); al.setContentsMargins(20,16,20,16)
            t = QLabel("✅ " + tr("schedule_active") if "schedule_active" in dir() else "✅ جدول نشط")
            t.setStyleSheet("color: #16A34A; font-size: 16px; font-weight: bold;"); al.addWidget(t)
            info = QLabel(f"📋 {active.name}\n⏱️ {active.created_at}\n📊 نقاط: {active.score}/100\n⚠️ تعارضات: {active.conflicts_count}\n❓ غير موزعة: {active.unassigned_count}")
            info.setStyleSheet("color: #E2E8F0; font-size: 13px;"); al.addWidget(info)
            cl.addWidget(ac)
        cl.addStretch(); scroll.setWidget(content); layout.addWidget(scroll,1)
    def refresh(self):
        for child in self.findChildren(QWidget): child.setParent(None); child.deleteLater()
        self._build_ui()
