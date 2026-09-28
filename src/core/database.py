# -*- coding: utf-8 -*-
"""قاعدة بيانات SQLite"""
import sqlite3, os
from pathlib import Path

DEFAULT_DB_PATH = Path.home() / ".school_scheduler" / "school_scheduler.db"

class Database:
    def __init__(self, db_path=None):
        self.db_path = str(db_path or DEFAULT_DB_PATH)
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA foreign_keys = ON;")
        self._init_schema()

    def _init_schema(self):
        c = self._conn.executescript
        
        c("""CREATE TABLE IF NOT EXISTS institution (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            name TEXT NOT NULL, year TEXT NOT NULL,
            use_fixed_rooms INTEGER DEFAULT 1,
            allow_free_periods INTEGER DEFAULT 0,
            distribute_subjects INTEGER DEFAULT 1,
            respect_teacher_hours INTEGER DEFAULT 1,
            language TEXT DEFAULT 'ar'
        );""")
        
        c("""CREATE TABLE IF NOT EXISTS cycles (
            id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE
        );""")
        
        c("""CREATE TABLE IF NOT EXISTS levels (
            id INTEGER PRIMARY KEY AUTOINCREMENT, cycle_id INTEGER NOT NULL, name TEXT NOT NULL,
            FOREIGN KEY (cycle_id) REFERENCES cycles(id) ON DELETE CASCADE,
            UNIQUE(cycle_id, name)
        );""")
        
        c("""CREATE TABLE IF NOT EXISTS sections (
            id INTEGER PRIMARY KEY AUTOINCREMENT, level_id INTEGER NOT NULL, name TEXT NOT NULL,
            fixed_room_id INTEGER,
            FOREIGN KEY (level_id) REFERENCES levels(id) ON DELETE CASCADE
        );""")
        
        c("""CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE,
            color TEXT DEFAULT '#6B7280', required_room_type TEXT
        );""")
        
        c("""CREATE TABLE IF NOT EXISTS subject_hours (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_id INTEGER NOT NULL, level_id INTEGER NOT NULL, hours_per_week INTEGER NOT NULL,
            FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE,
            FOREIGN KEY (level_id) REFERENCES levels(id) ON DELETE CASCADE,
            UNIQUE(subject_id, level_id)
        );""")
        
        c("""CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT, full_name TEXT NOT NULL,
            subject_id INTEGER NOT NULL, weekly_hours INTEGER DEFAULT 18,
            available_days TEXT DEFAULT '1,2,3,4,5',
            available_period TEXT DEFAULT 'both', notes TEXT
        );""")
        
        c("""CREATE TABLE IF NOT EXISTS teacher_sections (
            teacher_id INTEGER NOT NULL, section_id INTEGER NOT NULL,
            PRIMARY KEY (teacher_id, section_id)
        );""")
        
        c("""CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE,
            room_type TEXT DEFAULT 'regular', capacity INTEGER DEFAULT 40,
            available_days TEXT DEFAULT '1,2,3,4,5', available_period TEXT DEFAULT 'both'
        );""")
        
        c("""CREATE TABLE IF NOT EXISTS time_slots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day INTEGER CHECK (day BETWEEN 1 AND 5),
            period_type TEXT CHECK (period_type IN ('morning','evening')),
            start_time TEXT NOT NULL, end_time TEXT NOT NULL, slot_index INTEGER NOT NULL,
            UNIQUE(day, start_time, end_time)
        );""")
        
        c("""CREATE TABLE IF NOT EXISTS schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now','localtime')),
            is_active INTEGER DEFAULT 0, score REAL DEFAULT 0,
            conflicts_count INTEGER DEFAULT 0, unassigned_count INTEGER DEFAULT 0
        );""")
        
        c("""CREATE TABLE IF NOT EXISTS schedule_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT, schedule_id INTEGER NOT NULL,
            section_id INTEGER NOT NULL, subject_id INTEGER NOT NULL,
            teacher_id INTEGER NOT NULL, room_id INTEGER NOT NULL,
            time_slot_id INTEGER NOT NULL, session_duration INTEGER DEFAULT 1,
            is_locked INTEGER DEFAULT 0,
            FOREIGN KEY (schedule_id) REFERENCES schedules(id) ON DELETE CASCADE,
            UNIQUE(schedule_id, section_id, time_slot_id),
            UNIQUE(schedule_id, teacher_id, time_slot_id),
            UNIQUE(schedule_id, room_id, time_slot_id)
        );""")
        
        c("""CREATE TABLE IF NOT EXISTS locked_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            section_id INTEGER, subject_id INTEGER, teacher_id INTEGER,
            room_id INTEGER, time_slot_id INTEGER, session_duration INTEGER DEFAULT 1
        );""")
        
        c("""CREATE TABLE IF NOT EXISTS absences (
            id INTEGER PRIMARY KEY AUTOINCREMENT, teacher_id INTEGER NOT NULL,
            day INTEGER NOT NULL, period_type TEXT NOT NULL,
            substitute_teacher_id INTEGER, notes TEXT,
            created_at TEXT DEFAULT (datetime('now','localtime'))
        );""")
        
        cur = self._conn.execute("SELECT COUNT(*) FROM institution")
        if cur.fetchone()[0] == 0:
            self._conn.execute("INSERT INTO institution (id, name, year) VALUES (1, 'مدرستي', '2024-2025')")
        self._conn.commit()

    def execute(self, sql, params=()):
        cur = self._conn.execute(sql, params)
        self._conn.commit()
        return cur

    def query(self, sql, params=()):
        return [dict(r) for r in self._conn.execute(sql, params).fetchall()]

    def query_one(self, sql, params=()):
        r = self._conn.execute(sql, params).fetchone()
        return dict(r) if r else None

db = Database()
