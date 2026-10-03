# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QPushButton, QMessageBox, QScrollArea)
from PyQt5.QtCore import Qt
from src.core.i18n import tr
from src.core.database import db
from src.ui.widgets.page_header import PageHeader

class SettingsPage(QWidget):
    def __init__(self):
        super().__init__(); self._build_ui()
    def _build_ui(self):
        layout = QVBoxLayout(self); layout.setContentsMargins(0,0,0,0)
        layout.addWidget(PageHeader(tr("nav_constraints"), tr("constraints_hard")))
        scroll = QScrollArea(); scroll.setWidgetResizable(True); scroll.setFrameShape(QFrame.NoFrame)
        content = QWidget(); cl = QVBoxLayout(content); cl.setContentsMargins(24,16,24,24)
        # القيود الصلبة
        hc = QFrame(); hc.setObjectName("card"); hl = QVBoxLayout(hc); hl.setContentsMargins(24,20,24,20)
        ht = QLabel("🔒 " + tr("constraints_hard")); ht.setObjectName("cardTitle"); hl.addWidget(ht)
        for c in ["✓ لا أستاذ في قسمين بنفس الوقت","✓ لا قسم يدرس مادتين بنفس الوقت",
            "✓ لا قاعة تستقبل قسمين بنفس الوقت","✓ احترام الحجم الساعي الأسبوعي للأستاذ",
            "✓ اكتمال ساعات المادة لكل مستوى","✓ عدم وضع مادة في قاعة غير مناسبة",
            "✓ احترام القاعة الثابتة (إذا فُعِّلت)","✓ احترام أوقات الأستاذ","✓ احترام أوقات القاعة",
            "✓ وضع الحصص ضمن أوقات الدراسة","✓ عدم وجود فراغات بين الحصص (الصباح والمساء متتاليان)",
            "✓ لا تكرار نفس المادة مرتين في نفس اليوم",
            "✓ عدم الدراسة يوم الثلاثاء مساءً",
            "✓ لا تدرس المادة أكثر من ساعتين يوميًا",
            "✓ الرياضة تأتي كحصة واحدة (1h) أو حصتين متتاليتين (2h)"]:
            l = QLabel(c); l.setStyleSheet("color: #E2E8F0; padding: 4px 8px;"); hl.addWidget(l)
        cl.addWidget(hc)
        # القيود المرنة
        sc = QFrame(); sc.setObjectName("card"); sl = QVBoxLayout(sc); sl.setContentsMargins(24,20,24,20)
        st = QLabel("⚙️ " + tr("constraints_soft")); st.setObjectName("cardTitle"); sl.addWidget(st)
        for c in ["• تقليل الفراغات","• توزيع المواد على أيام الأسبوع","• تحسين استغلال القاعات","• تقليل انتقال التلاميذ"]:
            l = QLabel(c); l.setStyleSheet("color: #E2E8F0; padding: 4px 8px;"); sl.addWidget(l)
        cl.addWidget(sc)
        # إدارة البيانات
        dc = QFrame(); dc.setObjectName("card"); dl = QVBoxLayout(dc); dl.setContentsMargins(24,20,24,20)
        dt = QLabel("💾 إدارة البيانات"); dt.setObjectName("cardTitle"); dl.addWidget(dt)
        info = QLabel(f"قاعدة البيانات: {db.db_path}")
        info.setStyleSheet("color: #94A3B8; padding: 8px 0;"); info.setWordWrap(True); dl.addWidget(info)
        rb = QPushButton("🗑️ حذف كل البيانات"); rb.setObjectName("dangerButton")
        rb.clicked.connect(self._reset); dl.addWidget(rb)
        cl.addWidget(dc); cl.addStretch(); scroll.setWidget(content); layout.addWidget(scroll,1)
    def _reset(self):
        r = QMessageBox.warning(self, tr("confirm"), "⚠️ سيتم حذف كل البيانات نهائيًا!",
            QMessageBox.Yes | QMessageBox.No)
        if r == QMessageBox.Yes:
            for t in ["schedule_entries","schedules","absences","locked_sessions","time_slots",
                "teacher_sections","rooms","teachers","subject_hours","subjects","sections","levels","cycles"]:
                db.execute(f"DELETE FROM {t};")
            db.execute("DELETE FROM sqlite_sequence;")
            QMessageBox.information(self, tr("msg_saved"), "تم حذف كل البيانات")
    def refresh(self): pass
