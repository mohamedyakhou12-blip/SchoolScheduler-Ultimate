# -*- coding: utf-8 -*-
"""تصدير Excel فقط - v7.0 - تصميم احترافي"""
import os
from typing import List, Optional
from .models import (Schedule, ScheduleEntry, Section, Teacher, Room, Subject,
                     TimeSlot, Level, DAYS, ROOM_TYPES)
from .database import db
from .i18n import tr, get_language, is_rtl

try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    ARABIC_SHAPING_AVAILABLE = True
except ImportError:
    ARABIC_SHAPING_AVAILABLE = False

def shape_text(text):
    if not text or not ARABIC_SHAPING_AVAILABLE: return text
    try:
        if not any('\u0600' <= ch <= '\u06FF' for ch in text): return text
        return get_display(arabic_reshaper.reshape(text))
    except Exception: return text

def _color_to_rgb(hex_color):
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def get_section_grid(schedule_id, section_id):
    entries = ScheduleEntry.by_section(schedule_id, section_id)
    slots = TimeSlot.all()
    slot_by_id = {s.id: s for s in slots}
    subjects = {s.id: s for s in Subject.all()}
    teachers = {t.id: t for t in Teacher.all()}
    rooms = {r.id: r for r in Room.all()}
    grid = {d: {"morning": {}, "evening": {}} for d in range(1, 6)}
    for e in entries:
        slot = slot_by_id.get(e.time_slot_id)
        if not slot: continue
        grid.setdefault(slot.day, {}).setdefault(slot.period_type, {})[slot.id] = {
            "entry": e, "subject": subjects.get(e.subject_id),
            "teacher": teachers.get(e.teacher_id), "room": rooms.get(e.room_id), "slot": slot,
        }
    return grid, slots

def get_teacher_grid(schedule_id, teacher_id):
    entries = ScheduleEntry.by_teacher(schedule_id, teacher_id)
    slots = TimeSlot.all()
    slot_by_id = {s.id: s for s in slots}
    sections = {s.id: s for s in Section.all()}
    subjects = {s.id: s for s in Subject.all()}
    rooms = {r.id: r for r in Room.all()}
    grid = {d: {"morning": {}, "evening": {}} for d in range(1, 6)}
    for e in entries:
        slot = slot_by_id.get(e.time_slot_id)
        if not slot: continue
        grid.setdefault(slot.day, {}).setdefault(slot.period_type, {})[slot.id] = {
            "entry": e, "section": sections.get(e.section_id),
            "subject": subjects.get(e.subject_id), "room": rooms.get(e.room_id), "slot": slot,
        }
    return grid, slots

def get_room_grid(schedule_id, room_id):
    entries = ScheduleEntry.by_room(schedule_id, room_id)
    slots = TimeSlot.all()
    slot_by_id = {s.id: s for s in slots}
    sections = {s.id: s for s in Section.all()}
    subjects = {s.id: s for s in Subject.all()}
    teachers = {t.id: t for t in Teacher.all()}
    grid = {d: {"morning": {}, "evening": {}} for d in range(1, 6)}
    for e in entries:
        slot = slot_by_id.get(e.time_slot_id)
        if not slot: continue
        grid.setdefault(slot.day, {}).setdefault(slot.period_type, {})[slot.id] = {
            "entry": e, "section": sections.get(e.section_id),
            "subject": subjects.get(e.subject_id), "teacher": teachers.get(e.teacher_id), "slot": slot,
        }
    return grid, slots

def get_day_name(day, lang=None):
    lang = lang or get_language()
    for d in DAYS:
        if d[0] == day:
            return d[1] if lang == "ar" else d[2] if lang == "en" else d[3]
    return ""

def _fill_excel_cell(cell, cell_data, target_type):
    from openpyxl.styles import Font, PatternFill
    if target_type == "section":
        subj = cell_data.get("subject"); teacher = cell_data.get("teacher"); room = cell_data.get("room")
        parts = []
        if subj: parts.append(subj.name)
        if teacher: parts.append(teacher.full_name)
        if room: parts.append(f"[{room.name}]")
        cell.value = "\n".join(parts)
        if subj and subj.color:
            try:
                fc = subj.color.lstrip("#")
                r,g,b = int(fc[0:2],16),int(fc[2:4],16),int(fc[4:6],16)
                lr,lg,lb = int(r*0.3+255*0.7),int(g*0.3+255*0.7),int(b*0.3+255*0.7)
                lh = f"{lr:02X}{lg:02X}{lb:02X}"
                cell.fill = PatternFill(start_color=lh, end_color=lh, fill_type="solid")
                cell.font = Font(color="1F2937", bold=True, size=11, name="Tahoma")
            except: cell.font = Font(size=10, name="Tahoma")
        else: cell.font = Font(size=10, name="Tahoma")
    elif target_type == "teacher":
        section = cell_data.get("section"); subj = cell_data.get("subject"); room = cell_data.get("room")
        parts = []
        if section: parts.append(section.name)
        if subj: parts.append(subj.name)
        if room: parts.append(f"[{room.name}]")
        cell.value = "\n".join(parts)
        if subj and subj.color:
            try:
                fc = subj.color.lstrip("#")
                r,g,b = int(fc[0:2],16),int(fc[2:4],16),int(fc[4:6],16)
                lr,lg,lb = int(r*0.3+255*0.7),int(g*0.3+255*0.7),int(b*0.3+255*0.7)
                lh = f"{lr:02X}{lg:02X}{lb:02X}"
                cell.fill = PatternFill(start_color=lh, end_color=lh, fill_type="solid")
                cell.font = Font(color="1F2937", bold=True, size=11, name="Tahoma")
            except: cell.font = Font(size=10, name="Tahoma")
        else: cell.font = Font(size=10, name="Tahoma")
    elif target_type == "room":
        section = cell_data.get("section"); subj = cell_data.get("subject"); teacher = cell_data.get("teacher")
        parts = []
        if section: parts.append(section.name)
        if subj: parts.append(subj.name)
        if teacher: parts.append(teacher.full_name)
        cell.value = "\n".join(parts)
        if subj and subj.color:
            try:
                fc = subj.color.lstrip("#")
                r,g,b = int(fc[0:2],16),int(fc[2:4],16),int(fc[4:6],16)
                lr,lg,lb = int(r*0.3+255*0.7),int(g*0.3+255*0.7),int(b*0.3+255*0.7)
                lh = f"{lr:02X}{lg:02X}{lb:02X}"
                cell.fill = PatternFill(start_color=lh, end_color=lh, fill_type="solid")
                cell.font = Font(color="1F2937", bold=True, size=11, name="Tahoma")
            except: cell.font = Font(size=10, name="Tahoma")
        else: cell.font = Font(size=10, name="Tahoma")

def export_schedule_to_excel(schedule_id, target_type, target_id, output_path, lang=None):
    """تصدير جدول إلى Excel - تصميم احترافي v7.0"""
    lang = lang or get_language()
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter

    if target_type == "section":
        target = next((s for s in Section.all() if s.id == target_id), None)
        if not target: return None
        grid, slots = get_section_grid(schedule_id, target_id)
        title = f"جدول القسم: {target.name}"
    elif target_type == "teacher":
        target = next((t for t in Teacher.all() if t.id == target_id), None)
        if not target: return None
        grid, slots = get_teacher_grid(schedule_id, target_id)
        title = f"جدول الأستاذ: {target.full_name}"
    elif target_type == "room":
        target = next((r for r in Room.all() if r.id == target_id), None)
        if not target: return None
        grid, slots = get_room_grid(schedule_id, target_id)
        title = f"جدول القاعة: {target.name}"
    else: return None

    wb = Workbook(); ws = wb.active; ws.title = "Schedule"
    if is_rtl(): ws.sheet_view.rightToLeft = True

    # الألوان
    H_FILL = PatternFill("solid", start_color="1F2937")
    H_FONT = Font(color="FFFFFF", bold=True, size=12, name="Tahoma")
    D_FILL = PatternFill("solid", start_color="F3F4F6")
    D_FONT = Font(bold=True, size=11, color="1F2937", name="Tahoma")
    M_FILL = PatternFill("solid", start_color="DBEAFE")
    E_FILL = PatternFill("solid", start_color="FED7AA")
    B_FILL = PatternFill("solid", start_color="F59E0B")
    B_FONT = Font(color="FFFFFF", bold=True, size=10, name="Tahoma")
    BORDER = Border(*[Side("thin", color="9CA3AF")]*4)
    ALIGN = Alignment(horizontal="center", vertical="center", wrap_text=True)

    # ترتيب الحصص
    morning_slots = []; evening_slots = []; seen = set()
    for s in sorted(slots, key=lambda s: (s.period_type, s.slot_index)):
        key = (s.period_type, s.slot_index, s.start_time, s.end_time)
        if key not in seen:
            seen.add(key)
            if s.period_type == "morning": morning_slots.append(s)
            else: evening_slots.append(s)

    slots_by_day_period_idx = {(s.day, s.period_type, s.slot_index): s for s in slots}
    total_cols = 1 + len(morning_slots) + 1 + len(evening_slots)

    # الصف 1: العنوان
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=total_cols)
    tc = ws.cell(row=1, column=1, value=title)
    tc.font = Font(size=18, bold=True, color="FFFFFF", name="Tahoma")
    tc.alignment = ALIGN; tc.fill = PatternFill("solid", start_color="3B82F6")
    ws.row_dimensions[1].height = 40

    # الصف 2: معلومات
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=total_cols)
    sc = ws.cell(row=2, column=1, value="📅 الفترة الصباحية: 08:00 ← 12:00  |  🌅 الفترة المسائية: 13:30 ← 16:30")
    sc.font = Font(size=10, italic=True, color="6B7280", name="Tahoma")
    sc.alignment = ALIGN; sc.fill = PatternFill("solid", start_color="F9FAFB")
    ws.row_dimensions[2].height = 25

    # الصف 3: الرأس
    dh = ws.cell(row=3, column=1, value="اليوم")
    dh.fill = H_FILL; dh.font = H_FONT; dh.alignment = ALIGN; dh.border = BORDER
    for i, ts in enumerate(morning_slots):
        c = ws.cell(row=3, column=i+2, value=f"🕐 {ts.start_time} ← {ts.end_time}")
        c.fill = H_FILL; c.font = H_FONT; c.alignment = ALIGN; c.border = BORDER
    break_col = len(morning_slots) + 2
    bc = ws.cell(row=3, column=break_col, value="استراحة\n12:00\n13:30")
    bc.fill = B_FILL; bc.font = B_FONT; bc.alignment = ALIGN; bc.border = BORDER
    for i, ts in enumerate(evening_slots):
        c = ws.cell(row=3, column=break_col+1+i, value=f"🕐 {ts.start_time} ← {ts.end_time}")
        c.fill = H_FILL; c.font = H_FONT; c.alignment = ALIGN; c.border = BORDER
    ws.row_dimensions[3].height = 40

    # صفوف الأيام
    for day_idx, day in enumerate(range(1, 6)):
        row = day_idx + 4
        dc = ws.cell(row=row, column=1, value=get_day_name(day, lang))
        dc.font = D_FONT; dc.alignment = ALIGN; dc.border = BORDER; dc.fill = D_FILL
        for i, ts in enumerate(morning_slots):
            col = i + 2
            actual = slots_by_day_period_idx.get((day, ts.period_type, ts.slot_index))
            cd = grid.get(day, {}).get(ts.period_type, {}).get(actual.id) if actual else None
            c = ws.cell(row=row, column=col)
            c.alignment = ALIGN; c.border = BORDER; c.fill = M_FILL
            if cd: _fill_excel_cell(c, cd, target_type)
        brc = ws.cell(row=row, column=break_col, value="")
        brc.fill = PatternFill("solid", start_color="FEF3C7"); brc.border = BORDER
        for i, ts in enumerate(evening_slots):
            col = break_col + 1 + i
            actual = slots_by_day_period_idx.get((day, ts.period_type, ts.slot_index))
            cd = grid.get(day, {}).get(ts.period_type, {}).get(actual.id) if actual else None
            c = ws.cell(row=row, column=col)
            c.alignment = ALIGN; c.border = BORDER; c.fill = E_FILL
            if cd: _fill_excel_cell(c, cd, target_type)
        ws.row_dimensions[row].height = 65

    # عرض الأعمدة
    ws.column_dimensions["A"].width = 18
    for i in range(len(morning_slots)):
        ws.column_dimensions[get_column_letter(i + 2)].width = 22
    ws.column_dimensions[get_column_letter(break_col)].width = 8
    for i in range(len(evening_slots)):
        ws.column_dimensions[get_column_letter(break_col + 1 + i)].width = 22
    ws.freeze_panes = "B4"
    wb.save(output_path)
    return output_path

def _build_professional_sheet(ws, title, grid, slots, target_type, lang):
    """بناء ورقة Excel احترافية"""
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter
    H_FILL = PatternFill("solid", start_color="1F2937")
    H_FONT = Font(color="FFFFFF", bold=True, size=12, name="Tahoma")
    D_FILL = PatternFill("solid", start_color="F3F4F6")
    D_FONT = Font(bold=True, size=11, color="1F2937", name="Tahoma")
    M_FILL = PatternFill("solid", start_color="DBEAFE")
    E_FILL = PatternFill("solid", start_color="FED7AA")
    B_FILL = PatternFill("solid", start_color="F59E0B")
    B_FONT = Font(color="FFFFFF", bold=True, size=10, name="Tahoma")
    BORDER = Border(*[Side("thin", color="9CA3AF")]*4)
    ALIGN = Alignment(horizontal="center", vertical="center", wrap_text=True)
    if is_rtl(): ws.sheet_view.rightToLeft = True
    morning_slots = []; evening_slots = []; seen = set()
    for s in sorted(slots, key=lambda s: (s.period_type, s.slot_index)):
        key = (s.period_type, s.slot_index, s.start_time, s.end_time)
        if key not in seen:
            seen.add(key)
            if s.period_type == "morning": morning_slots.append(s)
            else: evening_slots.append(s)
    slots_by_day_period_idx = {(s.day, s.period_type, s.slot_index): s for s in slots}
    total_cols = 1 + len(morning_slots) + 1 + len(evening_slots)
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=total_cols)
    tc = ws.cell(row=1, column=1, value=title)
    tc.font = Font(size=16, bold=True, color="FFFFFF", name="Tahoma")
    tc.alignment = ALIGN; tc.fill = PatternFill("solid", start_color="3B82F6")
    ws.row_dimensions[1].height = 35
    dh = ws.cell(row=3, column=1, value="اليوم")
    dh.fill = H_FILL; dh.font = H_FONT; dh.alignment = ALIGN; dh.border = BORDER
    for i, ts in enumerate(morning_slots):
        c = ws.cell(row=3, column=i+2, value=f"🕐 {ts.start_time} ← {ts.end_time}")
        c.fill = H_FILL; c.font = H_FONT; c.alignment = ALIGN; c.border = BORDER
    break_col = len(morning_slots) + 2
    bc = ws.cell(row=3, column=break_col, value="استراحة\n12:00\n13:30")
    bc.fill = B_FILL; bc.font = B_FONT; bc.alignment = ALIGN; bc.border = BORDER
    for i, ts in enumerate(evening_slots):
        c = ws.cell(row=3, column=break_col+1+i, value=f"🕐 {ts.start_time} ← {ts.end_time}")
        c.fill = H_FILL; c.font = H_FONT; c.alignment = ALIGN; c.border = BORDER
    ws.row_dimensions[3].height = 40
    for day_idx, day in enumerate(range(1, 6)):
        row = day_idx + 4
        dc = ws.cell(row=row, column=1, value=get_day_name(day, lang))
        dc.font = D_FONT; dc.alignment = ALIGN; dc.border = BORDER; dc.fill = D_FILL
        for i, ts in enumerate(morning_slots):
            col = i + 2
            actual = slots_by_day_period_idx.get((day, ts.period_type, ts.slot_index))
            cd = grid.get(day, {}).get(ts.period_type, {}).get(actual.id) if actual else None
            c = ws.cell(row=row, column=col)
            c.alignment = ALIGN; c.border = BORDER; c.fill = M_FILL
            if cd: _fill_excel_cell(c, cd, target_type)
        brc = ws.cell(row=row, column=break_col, value="")
        brc.fill = PatternFill("solid", start_color="FEF3C7"); brc.border = BORDER
        for i, ts in enumerate(evening_slots):
            col = break_col + 1 + i
            actual = slots_by_day_period_idx.get((day, ts.period_type, ts.slot_index))
            cd = grid.get(day, {}).get(ts.period_type, {}).get(actual.id) if actual else None
            c = ws.cell(row=row, column=col)
            c.alignment = ALIGN; c.border = BORDER; c.fill = E_FILL
            if cd: _fill_excel_cell(c, cd, target_type)
        ws.row_dimensions[row].height = 65
    ws.column_dimensions["A"].width = 18
    for i in range(len(morning_slots)):
        ws.column_dimensions[get_column_letter(i + 2)].width = 22
    ws.column_dimensions[get_column_letter(break_col)].width = 8
    for i in range(len(evening_slots)):
        ws.column_dimensions[get_column_letter(break_col + 1 + i)].width = 22
    ws.freeze_panes = "B4"

def _create_index_sheet(wb, title, items, columns):
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter
    ws = wb.create_sheet("الفهرس")
    if is_rtl(): ws.sheet_view.rightToLeft = True
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(columns))
    tc = ws.cell(row=1, column=1, value=title)
    tc.font = Font(size=18, bold=True, color="FFFFFF", name="Tahoma")
    tc.alignment = Alignment(horizontal="center", vertical="center")
    tc.fill = PatternFill("solid", start_color="3B82F6")
    ws.row_dimensions[1].height = 40
    H_FILL = PatternFill("solid", start_color="1F2937")
    H_FONT = Font(color="FFFFFF", bold=True, size=12, name="Tahoma")
    ALIGN = Alignment(horizontal="center", vertical="center")
    BORDER = Border(*[Side("thin", color="9CA3AF")]*4)
    for i, col_name in enumerate(columns, start=1):
        c = ws.cell(row=3, column=i, value=col_name)
        c.fill = H_FILL; c.font = H_FONT; c.alignment = ALIGN; c.border = BORDER
    for row_idx, item in enumerate(items, start=4):
        for col_idx, value in enumerate(item, start=1):
            c = ws.cell(row=row_idx, column=col_idx, value=value)
            c.alignment = ALIGN; c.border = BORDER; c.font = Font(size=11, name="Tahoma")
        ws.row_dimensions[row_idx].height = 25
    for i, _ in enumerate(columns, start=1):
        ws.column_dimensions[get_column_letter(i)].width = 25

def export_all_sections_to_excel(schedule_id, output_path, lang=None):
    lang = lang or get_language()
    from openpyxl import Workbook
    sections = Section.all(); slots = TimeSlot.all()
    wb = Workbook(); wb.remove(wb.active)
    items = [(s.name, f"{s.cycle_name} - {s.level_name}", f"قسم {s.name}") for s in sections]
    _create_index_sheet(wb, "📋 فهرس جداول الأقسام", items, ["القسم", "المستوى", "اسم الورقة"])
    for sec in sections:
        ws = wb.create_sheet(f"قسم {sec.name}"[:30])
        grid, _ = get_section_grid(schedule_id, sec.id)
        _build_professional_sheet(ws, f"جدول القسم: {sec.name}", grid, slots, "section", lang)
    wb.save(output_path); return output_path

def export_all_teachers_to_excel(schedule_id, output_path, lang=None):
    lang = lang or get_language()
    from openpyxl import Workbook
    teachers_list = Teacher.all(); slots = TimeSlot.all()
    wb = Workbook(); wb.remove(wb.active)
    items = [(t.full_name, t.subject_name, f"{t.weekly_hours} ساعة") for t in teachers_list]
    _create_index_sheet(wb, "📋 فهرس جداول الأساتذة", items, ["الأستاذ", "المادة", "الحجم الساعي"])
    for t in teachers_list:
        ws = wb.create_sheet(t.full_name[:30])
        grid, _ = get_teacher_grid(schedule_id, t.id)
        _build_professional_sheet(ws, f"جدول الأستاذ: {t.full_name} ({t.subject_name})", grid, slots, "teacher", lang)
    wb.save(output_path); return output_path

def export_all_rooms_to_excel(schedule_id, output_path, lang=None):
    lang = lang or get_language()
    from openpyxl import Workbook
    rooms_list = Room.all(); slots = TimeSlot.all()
    room_type_names = dict((rt[0], rt[1]) for rt in ROOM_TYPES)
    wb = Workbook(); wb.remove(wb.active)
    items = [(r.name, room_type_names.get(r.room_type, r.room_type), str(r.capacity)) for r in rooms_list]
    _create_index_sheet(wb, "📋 فهرس جداول القاعات", items, ["القاعة", "النوع", "السعة"])
    for r in rooms_list:
        ws = wb.create_sheet(r.name[:30])
        grid, _ = get_room_grid(schedule_id, r.id)
        _build_professional_sheet(ws, f"جدول القاعة: {r.name}", grid, slots, "room", lang)
    wb.save(output_path); return output_path

def export_general_schedule_to_excel(schedule_id, output_path, lang=None):
    """الجدول العام - ورقة لكل يوم"""
    lang = lang or get_language()
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter
    sections = Section.all(); slots = TimeSlot.all()
    section_grids = {}
    for sec in sections:
        grid, _ = get_section_grid(schedule_id, sec.id); section_grids[sec.id] = grid
    morning_slots = []; evening_slots = []; seen = set()
    for s in sorted(slots, key=lambda s: (s.period_type, s.slot_index)):
        key = (s.period_type, s.slot_index, s.start_time, s.end_time)
        if key not in seen:
            seen.add(key)
            if s.period_type == "morning": morning_slots.append(s)
            else: evening_slots.append(s)
    slots_by_day_period_idx = {(s.day, s.period_type, s.slot_index): s for s in slots}
    days_ar = {1: "الأحد", 2: "الإثنين", 3: "الثلاثاء", 4: "الأربعاء", 5: "الخميس"}
    levels = Level.all()
    sections_by_level = {}
    for sec in sections: sections_by_level.setdefault(sec.level_id, []).append(sec)
    wb = Workbook(); wb.remove(wb.active)
    # فهرس
    index_ws = wb.create_sheet("الفهرس")
    if is_rtl(): index_ws.sheet_view.rightToLeft = True
    total_cols = 1 + len(morning_slots) + 1 + len(evening_slots)
    index_ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=4)
    tc = index_ws.cell(row=1, column=1, value="📋 الجدول العام للمؤسسة - الفهرس")
    tc.font = Font(size=18, bold=True, color="FFFFFF", name="Tahoma")
    tc.alignment = Alignment(horizontal="center", vertical="center")
    tc.fill = PatternFill("solid", start_color="3B82F6")
    index_ws.row_dimensions[1].height = 40
    for i, h in enumerate(["اليوم", "الوصف", "عدد الأقسام", "اسم الورقة"], start=1):
        c = index_ws.cell(row=3, column=i, value=h)
        c.fill = PatternFill("solid", start_color="1F2937")
        c.font = Font(color="FFFFFF", bold=True, size=12, name="Tahoma")
        c.alignment = Alignment(horizontal="center", vertical="center")
    for i, day in enumerate(range(1, 6), start=4):
        count = sum(1 for sec in sections if section_grids.get(sec.id, {}).get(day, {}).get("morning") or section_grids.get(sec.id, {}).get(day, {}).get("evening"))
        index_ws.cell(row=i, column=1, value=days_ar[day]).font = Font(bold=True, size=11, name="Tahoma")
        index_ws.cell(row=i, column=2, value=f"جدول كل أقسام {days_ar[day]}").font = Font(size=11, name="Tahoma")
        index_ws.cell(row=i, column=3, value=count).font = Font(size=11, name="Tahoma")
        index_ws.cell(row=i, column=4, value=days_ar[day]).font = Font(size=11, name="Tahoma")
    index_ws.column_dimensions["A"].width = 20; index_ws.column_dimensions["B"].width = 30
    index_ws.column_dimensions["C"].width = 15; index_ws.column_dimensions["D"].width = 20
    # ورقة لكل يوم
    H_FILL = PatternFill("solid", start_color="1F2937")
    H_FONT = Font(color="FFFFFF", bold=True, size=11, name="Tahoma")
    S_FILL = PatternFill("solid", start_color="F3F4F6")
    S_FONT = Font(bold=True, size=11, color="1F2937", name="Tahoma")
    M_FILL = PatternFill("solid", start_color="DBEAFE")
    E_FILL = PatternFill("solid", start_color="FED7AA")
    B_FILL = PatternFill("solid", start_color="F59E0B")
    B_FONT = Font(color="FFFFFF", bold=True, size=10, name="Tahoma")
    L_FILL = PatternFill("solid", start_color="8B5CF6")
    L_FONT = Font(size=13, bold=True, color="FFFFFF", name="Tahoma")
    BORDER = Border(*[Side("thin", color="9CA3AF")]*4)
    ALIGN = Alignment(horizontal="center", vertical="center", wrap_text=True)
    for day in range(1, 6):
        day_name = days_ar[day]
        ws = wb.create_sheet(day_name)
        if is_rtl(): ws.sheet_view.rightToLeft = True
        ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=total_cols)
        tc = ws.cell(row=1, column=1, value=f"📅 {day_name} - الجدول العام")
        tc.font = Font(size=16, bold=True, color="FFFFFF", name="Tahoma")
        tc.alignment = ALIGN; tc.fill = PatternFill("solid", start_color="3B82F6")
        ws.row_dimensions[1].height = 40
        sh = ws.cell(row=3, column=1, value="القسم")
        sh.fill = H_FILL; sh.font = H_FONT; sh.alignment = ALIGN; sh.border = BORDER
        for i, ts in enumerate(morning_slots):
            c = ws.cell(row=3, column=i+2, value=f"🕐 {ts.start_time} ← {ts.end_time}")
            c.fill = H_FILL; c.font = H_FONT; c.alignment = ALIGN; c.border = BORDER
        break_col = len(morning_slots) + 2
        bc = ws.cell(row=3, column=break_col, value="استراحة\n12:00\n13:30")
        bc.fill = B_FILL; bc.font = B_FONT; bc.alignment = ALIGN; bc.border = BORDER
        for i, ts in enumerate(evening_slots):
            c = ws.cell(row=3, column=break_col+1+i, value=f"🕐 {ts.start_time} ← {ts.end_time}")
            c.fill = H_FILL; c.font = H_FONT; c.alignment = ALIGN; c.border = BORDER
        ws.row_dimensions[3].height = 40
        current_row = 4
        for lvl in levels:
            lvl_sections = sections_by_level.get(lvl.id, [])
            if not lvl_sections: continue
            ws.merge_cells(start_row=current_row, start_column=1, end_row=current_row, end_column=total_cols)
            lc = ws.cell(row=current_row, column=1, value=f"📊 {lvl.cycle_name} - {lvl.name}")
            lc.font = L_FONT; lc.alignment = ALIGN; lc.fill = L_FILL; lc.border = BORDER
            ws.row_dimensions[current_row].height = 30; current_row += 1
            for sec in lvl_sections:
                grid = section_grids.get(sec.id, {})
                sc = ws.cell(row=current_row, column=1, value=sec.name)
                sc.font = S_FONT; sc.alignment = ALIGN; sc.border = BORDER; sc.fill = S_FILL
                for i, ts in enumerate(morning_slots):
                    col = i + 2
                    actual = slots_by_day_period_idx.get((day, ts.period_type, ts.slot_index))
                    cd = grid.get(day, {}).get(ts.period_type, {}).get(actual.id) if actual else None
                    c = ws.cell(row=current_row, column=col)
                    c.alignment = ALIGN; c.border = BORDER; c.fill = M_FILL
                    if cd: _fill_excel_cell(c, cd, "section")
                brc = ws.cell(row=current_row, column=break_col, value="")
                brc.fill = PatternFill("solid", start_color="FEF3C7"); brc.border = BORDER
                for i, ts in enumerate(evening_slots):
                    col = break_col + 1 + i
                    actual = slots_by_day_period_idx.get((day, ts.period_type, ts.slot_index))
                    cd = grid.get(day, {}).get(ts.period_type, {}).get(actual.id) if actual else None
                    c = ws.cell(row=current_row, column=col)
                    c.alignment = ALIGN; c.border = BORDER; c.fill = E_FILL
                    if cd: _fill_excel_cell(c, cd, "section")
                ws.row_dimensions[current_row].height = 60; current_row += 1
        ws.column_dimensions["A"].width = 15
        for i in range(len(morning_slots)): ws.column_dimensions[get_column_letter(i + 2)].width = 22
        ws.column_dimensions[get_column_letter(break_col)].width = 8
        for i in range(len(evening_slots)): ws.column_dimensions[get_column_letter(break_col + 1 + i)].width = 22
        ws.freeze_panes = "B4"
    wb.save(output_path); return output_path

def generate_print_html(schedule_id, target_type, target_id, lang=None):
    lang = lang or get_language()
    rtl = is_rtl(); dir_attr = "rtl" if rtl else "ltr"
    if target_type == "section":
        target = next((s for s in Section.all() if s.id == target_id), None)
        if not target: return ""
        grid, slots = get_section_grid(schedule_id, target_id)
        title = f"جدول القسم: {target.name}"
    elif target_type == "teacher":
        target = next((t for t in Teacher.all() if t.id == target_id), None)
        if not target: return ""
        grid, slots = get_teacher_grid(schedule_id, target_id)
        title = f"جدول الأستاذ: {target.full_name}"
    elif target_type == "room":
        target = next((r for r in Room.all() if r.id == target_id), None)
        if not target: return ""
        grid, slots = get_room_grid(schedule_id, target_id)
        title = f"جدول القاعة: {target.name}"
    else: return ""
    morning_slots = []; evening_slots = []; seen = set()
    for s in sorted(slots, key=lambda s: (s.period_type, s.slot_index)):
        key = (s.period_type, s.slot_index, s.start_time, s.end_time)
        if key not in seen:
            seen.add(key)
            if s.period_type == "morning": morning_slots.append(s)
            else: evening_slots.append(s)
    time_cols = morning_slots + evening_slots
    slots_by_day_period_idx = {(s.day, s.period_type, s.slot_index): s for s in slots}
    html = [f'<!DOCTYPE html><html lang="{lang}" dir="{dir_attr}"><head><meta charset="UTF-8">',
            f'<title>{title}</title><style>@page{{size:landscape;margin:10mm}}body{{font-family:Tahoma,Arial,sans-serif;margin:0;padding:10px}}',
            'h1{text-align:center;color:#1F2937;margin-bottom:5px}table{width:100%;border-collapse:collapse}',
            'th,td{border:1px solid #9CA3AF;padding:8px;text-align:center;font-size:11px}',
            'th{background:#1F2937;color:white;font-weight:bold}td.day-cell{background:#F3F4F6;font-weight:bold}',
            'td.empty{background:#FAFAFA;color:#D1D5DB}.cell-subject{font-weight:bold}',
            '.cell-teacher{font-size:9px;color:#4B5563}.cell-room{font-size:9px;color:#6B7280;font-style:italic}',
            '.break-cell{background:#F59E0B;color:white}</style></head><body>',
            f'<h1>{title}</h1><table><thead><tr><th>الاسم</th>']
    for ts in time_cols: html.append(f'<th>🕐 {ts.start_time} ← {ts.end_time}</th>')
    html.append('<th class="break-cell">استراحة</th>')
    for ts in evening_slots: html.append(f'<th>🕐 {ts.start_time} ← {ts.end_time}</th>')
    html.append('</tr></thead><tbody>')
    for day in range(1, 6):
        html.append(f'<tr><td class="day-cell">{get_day_name(day, lang)}</td>')
        for ts in morning_slots:
            actual = slots_by_day_period_idx.get((day, ts.period_type, ts.slot_index))
            cell = grid.get(day, {}).get(ts.period_type, {}).get(actual.id) if actual else None
            if cell:
                subj = cell.get("subject"); bg = f' style="background-color:{subj.color}40"' if subj and subj.color else ''
                parts = []
                if subj: parts.append(f'<div class="cell-subject">{subj.name}</div>')
                if cell.get("teacher"): parts.append(f'<div class="cell-teacher">{cell["teacher"].full_name}</div>')
                if cell.get("room"): parts.append(f'<div class="cell-room">[{cell["room"].name}]</div>')
                html.append(f'<td{bg}>{"".join(parts)}</td>')
            else: html.append('<td class="empty">—</td>')
        html.append('<td class="break-cell"></td>')
        for ts in evening_slots:
            actual = slots_by_day_period_idx.get((day, ts.period_type, ts.slot_index))
            cell = grid.get(day, {}).get(ts.period_type, {}).get(actual.id) if actual else None
            if cell:
                subj = cell.get("subject"); bg = f' style="background-color:{subj.color}40"' if subj and subj.color else ''
                parts = []
                if subj: parts.append(f'<div class="cell-subject">{subj.name}</div>')
                if cell.get("teacher"): parts.append(f'<div class="cell-teacher">{cell["teacher"].full_name}</div>')
                if cell.get("room"): parts.append(f'<div class="cell-room">[{cell["room"].name}]</div>')
                html.append(f'<td{bg}>{"".join(parts)}</td>')
            else: html.append('<td class="empty">—</td>')
        html.append('</tr>')
    html.append('</tbody></table></body></html>')
    return "\n".join(html)
