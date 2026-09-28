# -*- coding: utf-8 -*-
"""محرك الجدولة v7.0 - مع قيد عدم الفراغات + توزيع ذكي"""
import time, random
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set
from collections import defaultdict
from .database import db
from .models import (Schedule, ScheduleEntry, Section, Teacher, Room, Subject,
                     TimeSlot, LockedSession, Institution, DAYS)

@dataclass
class SchedulingTask:
    section_id: int; subject_id: int; teacher_id: int; hours_needed: int
    required_room_type: Optional[str] = None; level_id: int = 0

@dataclass
class SchedulingConfig:
    use_fixed_rooms: bool = True
    distribute_subjects: bool = True
    respect_teacher_hours: bool = True
    seed: Optional[int] = None
    max_sessions_per_day: int = 6
    max_teacher_sessions_per_day: int = 4

@dataclass
class SchedulingResult:
    schedule_id: int; success: bool; conflicts_count: int = 0
    unassigned_count: int = 0; unassigned_tasks: List[str] = field(default_factory=list)
    free_hours: float = 0; room_utilization: float = 0
    teacher_hours_ok: bool = True; score: float = 0; execution_time: float = 0

class SchedulingEngine:
    def __init__(self, config=None):
        self.config = config or SchedulingConfig()
        self.rng = random.Random(config.seed if config and config.seed else None)
        self.time_slots = []; self.sections = []; self.teachers = []
        self.rooms = []; self.subjects = []; self.subject_hours = {}
        self.locked_sessions = []; self.institution = None
        self.slots_by_day_period = defaultdict(list)
        self.rooms_by_type = defaultdict(list)
        self.teacher_by_id = {}; self.subject_by_id = {}
        self.room_by_id = {}; self.section_by_id = {}
        self.slot_by_id = {}; self.tasks = []

    def load_data(self):
        self.time_slots = TimeSlot.all(); self.sections = Section.all()
        self.teachers = Teacher.all(); self.rooms = Room.all()
        self.subjects = Subject.all(); self.locked_sessions = LockedSession.all()
        self.institution = Institution.load()
        for r in db.query("SELECT * FROM subject_hours"):
            self.subject_hours[(r["subject_id"], r["level_id"])] = r["hours_per_week"]
        for slot in self.time_slots:
            self.slots_by_day_period[(slot.day, slot.period_type)].append(slot)
            self.slot_by_id[slot.id] = slot
        for room in self.rooms:
            self.rooms_by_type[room.room_type].append(room); self.room_by_id[room.id] = room
        for sec in self.sections: self.section_by_id[sec.id] = sec
        for s in self.subjects: self.subject_by_id[s.id] = s
        for t in self.teachers: self.teacher_by_id[t.id] = t

    def build_tasks(self):
        tasks = []; teacher_load = {t.id: 0 for t in self.teachers}
        for section in self.sections:
            for subj in self.subjects:
                hours = self.subject_hours.get((subj.id, section.level_id), 0)
                if hours <= 0: continue
                candidates = [t for t in self.teachers if t.subject_id == subj.id and section.id in t.section_ids]
                if not candidates: continue
                teacher = min(candidates, key=lambda t: teacher_load.get(t.id, 0))
                teacher_load[teacher.id] += hours
                tasks.append(SchedulingTask(section_id=section.id, subject_id=subj.id,
                    teacher_id=teacher.id, hours_needed=hours,
                    required_room_type=subj.required_room_type, level_id=section.level_id))
        self.tasks = tasks; return tasks

    def _check_slot_conflict(self, grid, section_id, teacher_id, room_id, slot_id, duration=1):
        if (section_id, slot_id) in grid.get("sections", {}): return False
        if (teacher_id, slot_id) in grid.get("teachers", {}): return False
        if (room_id, slot_id) in grid.get("rooms", {}): return False
        if duration == 2:
            cur_slot = self.slot_by_id.get(slot_id)
            if not cur_slot: return False
            next_slot = self._find_next_consecutive_slot(cur_slot)
            if not next_slot: return False
            return self._check_slot_conflict(grid, section_id, teacher_id, room_id, next_slot.id, duration=1)
        return True

    def _find_next_consecutive_slot(self, slot):
        same_period = sorted(self.slots_by_day_period.get((slot.day, slot.period_type), []), key=lambda s: s.slot_index)
        for i, s in enumerate(same_period):
            if s.id == slot.id and i + 1 < len(same_period): return same_period[i + 1]
        return None

    def _would_create_gap(self, grid, section_id, slot_id):
        """قيد عدم الفراغات: لا فراغ بين الحصص في نفس الفترة"""
        slot = self.slot_by_id.get(slot_id)
        if not slot: return False
        same_period = sorted(self.slots_by_day_period.get((slot.day, slot.period_type), []), key=lambda s: s.slot_index)
        if not same_period: return False
        used_indices = set()
        for s in same_period:
            if (section_id, s.id) in grid.get("sections", {}): used_indices.add(s.slot_index)
        used_indices.add(slot.slot_index)
        if len(used_indices) <= 1: return False
        for idx in range(min(used_indices), max(used_indices) + 1):
            if idx not in used_indices: return True
        return False

    def _find_room_for_subject(self, subject, section):
        if self.config.use_fixed_rooms and not subject.required_room_type:
            if section.fixed_room_id:
                room = self.room_by_id.get(section.fixed_room_id)
                if room: return room
        if subject.required_room_type:
            candidates = self.rooms_by_type.get(subject.required_room_type, [])
            if candidates: return candidates[0]
        if self.config.use_fixed_rooms and section.fixed_room_id:
            room = self.room_by_id.get(section.fixed_room_id)
            if room: return room
        regular = self.rooms_by_type.get("regular", [])
        return regular[0] if regular else None

    def _split_hours_into_sessions(self, total_hours):
        """توزيع ذكي: 5س→[2,2,1], 4س→[2,2], 3س→[2,1], 2س→[2], 1س→[1]"""
        sessions = []
        while total_hours >= 2: sessions.append(2); total_hours -= 2
        if total_hours == 1: sessions.append(1)
        if self.config.distribute_subjects and len(sessions) > 1:
            self.rng.shuffle(sessions)
        return sessions

    def _get_candidate_slots(self, teacher, subject, room):
        teacher_days = set(teacher.days_list)
        teacher_periods = ["morning", "evening"] if teacher.available_period == "both" else [teacher.available_period]
        if room:
            common_days = teacher_days & set(room.days_list)
            room_periods = set(["morning","evening"] if room.available_period == "both" else [room.available_period])
            common_periods = set(teacher_periods) & room_periods
        else:
            common_days = teacher_days; common_periods = set(teacher_periods)
        candidates = []
        for day in common_days:
            for pt in common_periods:
                slots = list(self.slots_by_day_period.get((day, pt), []))
                self.rng.shuffle(slots)
                for s in slots: candidates.append(s.id)
        return candidates

    def schedule(self, name="جدول جديد"):
        start_time = time.time()
        self.load_data(); self.build_tasks()
        sorted_tasks = sorted(self.tasks, key=lambda t: (-(1 if t.required_room_type else 0), -t.hours_needed))
        schedule = Schedule(name=name, is_active=False); schedule.save()
        schedule_id = schedule.id
        grid = {"sections": {}, "teachers": {}, "rooms": {}}
        teacher_used_hours = defaultdict(int)
        # إدراج الحصص المقفلة
        for lock in self.locked_sessions:
            entry = ScheduleEntry(schedule_id=schedule_id, section_id=lock.section_id, subject_id=lock.subject_id,
                teacher_id=lock.teacher_id, room_id=lock.room_id, time_slot_id=lock.time_slot_id,
                session_duration=lock.session_duration, is_locked=True)
            entry.save()
            grid["sections"][(lock.section_id, lock.time_slot_id)] = entry
            grid["teachers"][(lock.teacher_id, lock.time_slot_id)] = entry
            grid["rooms"][(lock.room_id, lock.time_slot_id)] = entry
            teacher_used_hours[lock.teacher_id] += lock.session_duration
        # جدولة المهام
        unassigned_tasks = []; assigned_entries = []
        teachers_by_subject = defaultdict(list)
        for t in self.teachers: teachers_by_subject[t.subject_id].append(t)
        # تتبع الحصص اليومية للقسم والأستاذ
        section_daily_count = defaultdict(lambda: defaultdict(int))
        teacher_daily_count = defaultdict(lambda: defaultdict(int))
        section_daily_subjects = defaultdict(lambda: defaultdict(set))

        for task in sorted_tasks:
            teacher = self.teacher_by_id.get(task.teacher_id)
            section = self.section_by_id.get(task.section_id)
            subject = self.subject_by_id.get(task.subject_id)
            if not teacher or not section or not subject: continue
            if self.config.respect_teacher_hours:
                remaining = teacher.weekly_hours - teacher_used_hours.get(teacher.id, 0)
                if remaining <= 0:
                    alt = next((at for at in teachers_by_subject.get(subject.id, [])
                               if at.id != teacher.id and section.id in at.section_ids
                               and at.weekly_hours - teacher_used_hours.get(at.id, 0) > 0), None)
                    if alt: teacher = alt; remaining = teacher.weekly_hours - teacher_used_hours.get(teacher.id, 0)
                    else: unassigned_tasks.append(f"تجاوز الحجم: {teacher.full_name} - {subject.name}"); continue
                hours_to_assign = min(task.hours_needed, remaining)
            else: hours_to_assign = task.hours_needed
            sessions = self._split_hours_into_sessions(hours_to_assign)
            assigned_room = self._find_room_for_subject(subject, section)

            for session_duration in sessions:
                placed = False
                candidate_slots = self._get_candidate_slots(teacher, subject, assigned_room)
                for slot_id in candidate_slots:
                    if not self._check_slot_conflict(grid, section.id,
                        teacher.id, assigned_room.id if assigned_room else 0, slot_id, session_duration): continue
                    if assigned_room and not self._check_room_available(assigned_room,
                        self.slot_by_id[slot_id].day, self.slot_by_id[slot_id].period_type): continue
                    if self._would_create_gap(grid, section.id, slot_id): continue
                    # لا حد أقصى للحصص اليومية - يمكن حتى 8 ساعات
                    day = self.slot_by_id[slot_id].day
                    # قيد: لا تكرار نفس المادة مرتين في نفس اليوم (إلا إذا كانت 2h متتالية)
                    if subject.id in section_daily_subjects[section.id][day] and session_duration != 2: continue
                    room_id = assigned_room.id if assigned_room else 0
                    entry = ScheduleEntry(schedule_id=schedule_id, section_id=section.id, subject_id=subject.id,
                        teacher_id=teacher.id, room_id=room_id, time_slot_id=slot_id,
                        session_duration=session_duration, is_locked=False)
                    entry.save()
                    grid["sections"][(section.id, slot_id)] = entry
                    grid["teachers"][(teacher.id, slot_id)] = entry
                    grid["rooms"][(room_id, slot_id)] = entry
                    teacher_used_hours[teacher.id] += session_duration
                    assigned_entries.append(entry)
                    section_daily_count[section.id][day] += 1
                    teacher_daily_count[teacher.id][day] += 1
                    section_daily_subjects[section.id][day].add(subject.id)
                    placed = True; break
                if not placed:
                    # محاولة بديل
                    alt_placed = False
                    for at in teachers_by_subject.get(subject.id, []):
                        if at.id == teacher.id or section.id not in at.section_ids: continue
                        at_rem = at.weekly_hours - teacher_used_hours.get(at.id, 0)
                        if at_rem < session_duration: continue
                        cs2 = self._get_candidate_slots(at, subject, assigned_room)
                        for sid in cs2:
                            if not self._check_slot_conflict(grid, section.id, at.id,
                                assigned_room.id if assigned_room else 0, sid, session_duration): continue
                            if assigned_room and not self._check_room_available(assigned_room,
                                self.slot_by_id[sid].day, self.slot_by_id[sid].period_type): continue
                            if self._would_create_gap(grid, section.id, sid): continue
                            day = self.slot_by_id[sid].day
                            # لا حد أقصى للحصص اليومية - يمكن حتى 8 ساعات
                            if subject.id in section_daily_subjects[section.id][day] and session_duration != 2: continue
                            room_id = assigned_room.id if assigned_room else 0
                            entry = ScheduleEntry(schedule_id=schedule_id, section_id=section.id, subject_id=subject.id,
                                teacher_id=at.id, room_id=room_id, time_slot_id=sid,
                                session_duration=session_duration, is_locked=False)
                            entry.save()
                            grid["sections"][(section.id, sid)] = entry
                            grid["teachers"][(at.id, sid)] = entry
                            grid["rooms"][(room_id, sid)] = entry
                            teacher_used_hours[at.id] += session_duration
                            assigned_entries.append(entry)
                            section_daily_count[section.id][day] += 1
                            teacher_daily_count[at.id][day] += 1
                            section_daily_subjects[section.id][day].add(subject.id)
                            alt_placed = True; break
                        if alt_placed: break
                    if not alt_placed:
                        unassigned_tasks.append(f"تعذر: {section.name} - {subject.name} ({session_duration}س) - {teacher.full_name}")
        # المؤشرات
        execution_time = time.time() - start_time
        conflicts_count = self._count_conflicts(schedule_id)
        score = self._calculate_score(conflicts_count, len(unassigned_tasks), len(self.tasks))
        schedule.score = score; schedule.conflicts_count = conflicts_count
        schedule.unassigned_count = len(unassigned_tasks); schedule.save()
        return SchedulingResult(schedule_id=schedule_id, success=(conflicts_count == 0 and len(unassigned_tasks) == 0),
            conflicts_count=conflicts_count, unassigned_count=len(unassigned_tasks),
            unassigned_tasks=unassigned_tasks, score=score, execution_time=execution_time)

    def _check_room_available(self, room, day, period_type):
        if day not in room.days_list: return False
        if room.available_period == "both": return True
        return room.available_period == period_type

    def _count_conflicts(self, schedule_id):
        s = len(db.query("""SELECT section_id, time_slot_id FROM schedule_entries WHERE schedule_id=?
            GROUP BY section_id, time_slot_id HAVING COUNT(*) > 1""", (schedule_id,)))
        t = len(db.query("""SELECT teacher_id, time_slot_id FROM schedule_entries WHERE schedule_id=?
            GROUP BY teacher_id, time_slot_id HAVING COUNT(*) > 1""", (schedule_id,)))
        r = len(db.query("""SELECT room_id, time_slot_id FROM schedule_entries WHERE schedule_id=? AND room_id > 0
            GROUP BY room_id, time_slot_id HAVING COUNT(*) > 1""", (schedule_id,)))
        return s + t + r

    def _calculate_score(self, conflicts, unassigned, total_tasks):
        score = 100.0 - conflicts * 30
        if total_tasks > 0:
            score -= (unassigned / max(total_tasks, 1)) * 60
        else:
            score -= unassigned * 2
        return round(max(0, min(100, score)), 2)

def check_conflict(section_id, teacher_id, room_id, time_slot_id, schedule_id, exclude_entry_id=None):
    q = "SELECT se.id, s.name as section_name, sub.name as subject_name FROM schedule_entries se LEFT JOIN sections s ON se.section_id = s.id LEFT JOIN subjects sub ON se.subject_id = sub.id WHERE se.schedule_id=? AND se.section_id=? AND se.time_slot_id=?"
    params = [schedule_id, section_id, time_slot_id]
    if exclude_entry_id: q += " AND se.id != ?"; params.append(exclude_entry_id)
    r = db.query_one(q, tuple(params))
    if r: return f"⚠️ القسم مشغول: {r['subject_name']}"
    q = "SELECT se.id, t.full_name as teacher_name FROM schedule_entries se LEFT JOIN teachers t ON se.teacher_id = t.id WHERE se.schedule_id=? AND se.teacher_id=? AND se.time_slot_id=?"
    params = [schedule_id, teacher_id, time_slot_id]
    if exclude_entry_id: q += " AND se.id != ?"; params.append(exclude_entry_id)
    r = db.query_one(q, tuple(params))
    if r: return f"⚠️ الأستاذ {r['teacher_name']} مشغول"
    if room_id and room_id > 0:
        q = "SELECT se.id, sec.name as section_name FROM schedule_entries se LEFT JOIN sections sec ON se.section_id = sec.id WHERE se.schedule_id=? AND se.room_id=? AND se.time_slot_id=?"
        params = [schedule_id, room_id, time_slot_id]
        if exclude_entry_id: q += " AND se.id != ?"; params.append(exclude_entry_id)
        r = db.query_one(q, tuple(params))
        if r: return f"⚠️ القاعة مشغولة: {r['section_name']}"
    return None

def find_substitute_teacher(teacher_id, day, period_type, subject_id=None):
    candidates = []
    for t in Teacher.all():
        if t.id == teacher_id: continue
        if subject_id and t.subject_id != subject_id: continue
        if day not in t.days_list: continue
        if t.available_period != "both" and t.available_period != period_type: continue
        candidates.append(t)
    return candidates
