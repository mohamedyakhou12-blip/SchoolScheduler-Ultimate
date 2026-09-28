# -*- coding: utf-8 -*-
"""النماذج - v7.0 (بدون session_type)"""
from dataclasses import dataclass, field
from typing import Optional, List
from .database import db

DAYS = [
    (1, "الأحد", "Sunday", "Dimanche"),
    (2, "الإثنين", "Monday", "Lundi"),
    (3, "الثلاثاء", "Tuesday", "Mardi"),
    (4, "الأربعاء", "Wednesday", "Mercredi"),
    (5, "الخميس", "Thursday", "Jeudi"),
]
PERIOD_TYPES = [("morning","الفترة الصباحية"),("evening","الفترة المسائية")]
ROOM_TYPES = [
    ("regular","قاعة عادية"),("science","مخبر العلوم"),
    ("physics","مخبر الفيزياء"),("computer","مخبر الإعلام الآلي"),
    ("sport","قاعة الرياضة"),("other","أخرى"),
]

@dataclass
class Institution:
    id: int = 1; name: str = ""; year: str = ""
    use_fixed_rooms: bool = True; allow_free_periods: bool = False
    distribute_subjects: bool = True; respect_teacher_hours: bool = True
    language: str = "ar"
    @classmethod
    def load(cls):
        r = db.query_one("SELECT * FROM institution WHERE id=1")
        if not r: return cls()
        return cls(id=r["id"], name=r["name"], year=r["year"],
                   use_fixed_rooms=bool(r["use_fixed_rooms"]),
                   allow_free_periods=bool(r["allow_free_periods"]),
                   distribute_subjects=bool(r["distribute_subjects"]),
                   respect_teacher_hours=bool(r["respect_teacher_hours"]),
                   language=r["language"])
    def save(self):
        db.execute("""UPDATE institution SET name=?,year=?,use_fixed_rooms=?,allow_free_periods=?,
            distribute_subjects=?,respect_teacher_hours=?,language=? WHERE id=1""",
            (self.name,self.year,int(self.use_fixed_rooms),int(self.allow_free_periods),
             int(self.distribute_subjects),int(self.respect_teacher_hours),self.language))

@dataclass
class Cycle:
    id: Optional[int] = None; name: str = ""
    @classmethod
    def all(cls): return [cls(id=r["id"],name=r["name"]) for r in db.query("SELECT * FROM cycles ORDER BY name")]
    @classmethod
    def get(cls,i): r=db.query_one("SELECT * FROM cycles WHERE id=?",i and (i,)); return cls(id=r["id"],name=r["name"]) if r else None
    def save(self):
        if self.id: db.execute("UPDATE cycles SET name=? WHERE id=?", (self.name,self.id))
        else: self.id=db.execute("INSERT INTO cycles (name) VALUES (?)",(self.name,)).lastrowid
    def delete(self):
        if self.id: db.execute("DELETE FROM cycles WHERE id=?", (self.id,)); self.id=None

@dataclass
class Level:
    id: Optional[int] = None; cycle_id: int = 0; name: str = ""; cycle_name: str = ""
    @classmethod
    def all(cls):
        return [cls(id=r["id"],cycle_id=r["cycle_id"],name=r["name"],cycle_name=r.get("cycle_name",""))
                for r in db.query("""SELECT l.*,c.name as cycle_name FROM levels l
                LEFT JOIN cycles c ON l.cycle_id=c.id ORDER BY c.name,l.name""")]
    @classmethod
    def by_cycle(cls,cid): return [cls(id=r["id"],cycle_id=r["cycle_id"],name=r["name"]) for r in db.query("SELECT * FROM levels WHERE cycle_id=? ORDER BY name",(cid,))]
    def save(self):
        if self.id: db.execute("UPDATE levels SET cycle_id=?,name=? WHERE id=?", (self.cycle_id,self.name,self.id))
        else: self.id=db.execute("INSERT INTO levels (cycle_id,name) VALUES (?,?)",(self.cycle_id,self.name)).lastrowid
    def delete(self):
        if self.id: db.execute("DELETE FROM levels WHERE id=?", (self.id,)); self.id=None

@dataclass
class Section:
    id: Optional[int] = None; level_id: int = 0; name: str = ""
    fixed_room_id: Optional[int] = None; level_name: str = ""; cycle_name: str = ""
    @classmethod
    def all(cls):
        return [cls(id=r["id"],level_id=r["level_id"],name=r["name"],fixed_room_id=r["fixed_room_id"],
                level_name=r.get("level_name",""),cycle_name=r.get("cycle_name",""))
                for r in db.query("""SELECT s.*,l.name as level_name,c.name as cycle_name
                FROM sections s LEFT JOIN levels l ON s.level_id=l.id LEFT JOIN cycles c ON l.cycle_id=c.id
                ORDER BY c.name,l.name,s.name""")]
    def save(self):
        if self.id: db.execute("UPDATE sections SET level_id=?,name=?,fixed_room_id=? WHERE id=?", (self.level_id,self.name,self.fixed_room_id,self.id))
        else: self.id=db.execute("INSERT INTO sections (level_id,name,fixed_room_id) VALUES (?,?,?)",(self.level_id,self.name,self.fixed_room_id)).lastrowid
    def delete(self):
        if self.id: db.execute("DELETE FROM sections WHERE id=?", (self.id,)); self.id=None

@dataclass
class Subject:
    id: Optional[int] = None; name: str = ""; color: str = "#6B7280"
    required_room_type: Optional[str] = None
    @classmethod
    def all(cls): return [cls(id=r["id"],name=r["name"],color=r["color"],required_room_type=r["required_room_type"]) for r in db.query("SELECT * FROM subjects ORDER BY name")]
    @classmethod
    def get(cls,i):
        r=db.query_one("SELECT * FROM subjects WHERE id=?", i and (i,))
        return cls(id=r["id"],name=r["name"],color=r["color"],required_room_type=r["required_room_type"]) if r else None
    def save(self):
        if self.id: db.execute("UPDATE subjects SET name=?,color=?,required_room_type=? WHERE id=?", (self.name,self.color,self.required_room_type,self.id))
        else: self.id=db.execute("INSERT INTO subjects (name,color,required_room_type) VALUES (?,?,?)",(self.name,self.color,self.required_room_type)).lastrowid
    def delete(self):
        if self.id: db.execute("DELETE FROM subjects WHERE id=?", (self.id,)); self.id=None

@dataclass
class SubjectHour:
    id: Optional[int] = None; subject_id: int = 0; level_id: int = 0; hours_per_week: int = 0
    @classmethod
    def by_subject_level(cls,sid,lid):
        r=db.query_one("SELECT * FROM subject_hours WHERE subject_id=? AND level_id=?", (sid,lid))
        return cls(id=r["id"],subject_id=r["subject_id"],level_id=r["level_id"],hours_per_week=r["hours_per_week"]) if r else None
    def save(self):
        ex=db.query_one("SELECT id FROM subject_hours WHERE subject_id=? AND level_id=?", (self.subject_id,self.level_id))
        if ex: db.execute("UPDATE subject_hours SET hours_per_week=? WHERE id=?", (self.hours_per_week,ex["id"]))
        else: self.id=db.execute("INSERT INTO subject_hours (subject_id,level_id,hours_per_week) VALUES (?,?,?)",(self.subject_id,self.level_id,self.hours_per_week)).lastrowid

@dataclass
class Teacher:
    id: Optional[int] = None; full_name: str = ""; subject_id: int = 0
    weekly_hours: int = 18; available_days: str = "1,2,3,4,5"
    available_period: str = "both"; notes: str = ""
    section_ids: List[int] = field(default_factory=list); subject_name: str = ""
    @classmethod
    def all(cls):
        result=[]
        for r in db.query("""SELECT t.*,s.name as subject_name FROM teachers t
            LEFT JOIN subjects s ON t.subject_id=s.id ORDER BY t.full_name"""):
            t=cls(id=r["id"],full_name=r["full_name"],subject_id=r["subject_id"],
                  weekly_hours=r["weekly_hours"],available_days=r["available_days"],
                  available_period=r["available_period"],notes=r["notes"] or "",subject_name=r["subject_name"] or "")
            t.section_ids=[x["section_id"] for x in db.query("SELECT section_id FROM teacher_sections WHERE teacher_id=?", (t.id,))]
            result.append(t)
        return result
    @classmethod
    def get(cls,i):
        r=db.query_one("SELECT t.*,s.name as subject_name FROM teachers t LEFT JOIN subjects s ON t.subject_id=s.id WHERE t.id=?", i and (i,))
        if not r: return None
        t=cls(id=r["id"],full_name=r["full_name"],subject_id=r["subject_id"],weekly_hours=r["weekly_hours"],
              available_days=r["available_days"],available_period=r["available_period"],notes=r["notes"] or "",subject_name=r["subject_name"] or "")
        t.section_ids=[x["section_id"] for x in db.query("SELECT section_id FROM teacher_sections WHERE teacher_id=?", (t.id,))]
        return t
    def save(self):
        if self.id: db.execute("""UPDATE teachers SET full_name=?,subject_id=?,weekly_hours=?,available_days=?,available_period=?,notes=? WHERE id=?""",
            (self.full_name,self.subject_id,self.weekly_hours,self.available_days,self.available_period,self.notes,self.id))
        else: self.id=db.execute("""INSERT INTO teachers (full_name,subject_id,weekly_hours,available_days,available_period,notes) VALUES (?,?,?,?,?,?)""",
            (self.full_name,self.subject_id,self.weekly_hours,self.available_days,self.available_period,self.notes)).lastrowid
        db.execute("DELETE FROM teacher_sections WHERE teacher_id=?", (self.id,))
        for sid in self.section_ids: db.execute("INSERT INTO teacher_sections (teacher_id,section_id) VALUES (?,?)", (self.id,sid))
    def delete(self):
        if self.id: db.execute("DELETE FROM teachers WHERE id=?", (self.id,)); self.id=None
    @property
    def days_list(self): return [int(x) for x in self.available_days.split(",") if x.strip()]
    @days_list.setter
    def days_list(self,d): self.available_days=",".join(str(x) for x in d)

@dataclass
class Room:
    id: Optional[int] = None; name: str = ""; room_type: str = "regular"
    capacity: int = 40; available_days: str = "1,2,3,4,5"; available_period: str = "both"
    @classmethod
    def all(cls): return [cls(id=r["id"],name=r["name"],room_type=r["room_type"],capacity=r["capacity"],
        available_days=r["available_days"],available_period=r["available_period"]) for r in db.query("SELECT * FROM rooms ORDER BY name")]
    @classmethod
    def get(cls,i):
        r=db.query_one("SELECT * FROM rooms WHERE id=?", i and (i,))
        return cls(id=r["id"],name=r["name"],room_type=r["room_type"],capacity=r["capacity"],
            available_days=r["available_days"],available_period=r["available_period"]) if r else None
    def save(self):
        if self.id: db.execute("UPDATE rooms SET name=?,room_type=?,capacity=?,available_days=?,available_period=? WHERE id=?",
            (self.name,self.room_type,self.capacity,self.available_days,self.available_period,self.id))
        else: self.id=db.execute("INSERT INTO rooms (name,room_type,capacity,available_days,available_period) VALUES (?,?,?,?,?)",
            (self.name,self.room_type,self.capacity,self.available_days,self.available_period)).lastrowid
    def delete(self):
        if self.id: db.execute("DELETE FROM rooms WHERE id=?", (self.id,)); self.id=None
    @property
    def days_list(self): return [int(x) for x in self.available_days.split(",") if x.strip()]

@dataclass
class TimeSlot:
    id: Optional[int] = None; day: int = 1; period_type: str = "morning"
    start_time: str = ""; end_time: str = ""; slot_index: int = 0
    @classmethod
    def all(cls): return [cls(id=r["id"],day=r["day"],period_type=r["period_type"],
        start_time=r["start_time"],end_time=r["end_time"],slot_index=r["slot_index"])
        for r in db.query("SELECT * FROM time_slots ORDER BY day,period_type,slot_index")]
    @classmethod
    def count(cls):
        r=db.query_one("SELECT COUNT(*) as c FROM time_slots"); return r["c"] if r else 0
    @classmethod
    def initialize_default(cls):
        db.execute("DELETE FROM time_slots")
        for day in range(1,6):
            for st,et,idx,pt in [("08:00","09:00",0,"morning"),("09:00","10:00",1,"morning"),
                ("10:00","11:00",2,"morning"),("11:00","12:00",3,"morning"),
                ("13:30","14:30",0,"evening"),("14:30","15:30",1,"evening"),("15:30","16:30",2,"evening")]:
                db.execute("INSERT INTO time_slots (day,period_type,start_time,end_time,slot_index) VALUES (?,?,?,?,?)",(day,pt,st,et,idx))

@dataclass
class Schedule:
    id: Optional[int] = None; name: str = ""; created_at: str = ""
    is_active: bool = False; score: float = 0; conflicts_count: int = 0; unassigned_count: int = 0
    @classmethod
    def all(cls):
        result=[]
        for r in db.query("SELECT * FROM schedules ORDER BY created_at DESC"):
            result.append(cls(id=r["id"],name=r["name"],created_at=r["created_at"],
                is_active=bool(r["is_active"]),score=r["score"],
                conflicts_count=r["conflicts_count"],unassigned_count=r["unassigned_count"]))
        return result
    @classmethod
    def get(cls,i):
        r=db.query_one("SELECT * FROM schedules WHERE id=?", i and (i,))
        return cls(id=r["id"],name=r["name"],created_at=r["created_at"],is_active=bool(r["is_active"]),
            score=r["score"],conflicts_count=r["conflicts_count"],unassigned_count=r["unassigned_count"]) if r else None
    def save(self):
        if self.id: db.execute("UPDATE schedules SET name=?,is_active=?,score=?,conflicts_count=?,unassigned_count=? WHERE id=?",
            (self.name,int(self.is_active),self.score,self.conflicts_count,self.unassigned_count,self.id))
        else: self.id=db.execute("INSERT INTO schedules (name,is_active,score,conflicts_count,unassigned_count) VALUES (?,?,?,?,?)",
            (self.name,int(self.is_active),self.score,self.conflicts_count,self.unassigned_count)).lastrowid
    def delete(self):
        if self.id: db.execute("DELETE FROM schedules WHERE id=?", (self.id,)); self.id=None
    @classmethod
    def set_active(cls,i): db.execute("UPDATE schedules SET is_active=0"); db.execute("UPDATE schedules SET is_active=1 WHERE id=?", (i,))

@dataclass
class ScheduleEntry:
    id: Optional[int] = None; schedule_id: int = 0; section_id: int = 0
    subject_id: int = 0; teacher_id: int = 0; room_id: int = 0
    time_slot_id: int = 0; session_duration: int = 1; is_locked: bool = False
    @classmethod
    def by_schedule(cls,sid):
        return [cls(id=r["id"],schedule_id=r["schedule_id"],section_id=r["section_id"],
            subject_id=r["subject_id"],teacher_id=r["teacher_id"],room_id=r["room_id"],
            time_slot_id=r["time_slot_id"],session_duration=r["session_duration"],is_locked=bool(r["is_locked"]))
            for r in db.query("SELECT * FROM schedule_entries WHERE schedule_id=? ORDER BY section_id,time_slot_id", (sid,))]
    @classmethod
    def by_section(cls,sid,secid):
        return [cls(id=r["id"],schedule_id=r["schedule_id"],section_id=r["section_id"],
            subject_id=r["subject_id"],teacher_id=r["teacher_id"],room_id=r["room_id"],
            time_slot_id=r["time_slot_id"],session_duration=r["session_duration"],is_locked=bool(r["is_locked"]))
            for r in db.query("SELECT * FROM schedule_entries WHERE schedule_id=? AND section_id=? ORDER BY time_slot_id", (sid,secid))]
    @classmethod
    def by_teacher(cls,sid,tid):
        return [cls(id=r["id"],schedule_id=r["schedule_id"],section_id=r["section_id"],
            subject_id=r["subject_id"],teacher_id=r["teacher_id"],room_id=r["room_id"],
            time_slot_id=r["time_slot_id"],session_duration=r["session_duration"],is_locked=bool(r["is_locked"]))
            for r in db.query("SELECT * FROM schedule_entries WHERE schedule_id=? AND teacher_id=? ORDER BY time_slot_id", (sid,tid))]
    @classmethod
    def by_room(cls,sid,rid):
        return [cls(id=r["id"],schedule_id=r["schedule_id"],section_id=r["section_id"],
            subject_id=r["subject_id"],teacher_id=r["teacher_id"],room_id=r["room_id"],
            time_slot_id=r["time_slot_id"],session_duration=r["session_duration"],is_locked=bool(r["is_locked"]))
            for r in db.query("SELECT * FROM schedule_entries WHERE schedule_id=? AND room_id=? ORDER BY time_slot_id", (sid,rid))]
    def save(self):
        self.id=db.execute("""INSERT INTO schedule_entries
            (schedule_id,section_id,subject_id,teacher_id,room_id,time_slot_id,session_duration,is_locked)
            VALUES (?,?,?,?,?,?,?,?)""",
            (self.schedule_id,self.section_id,self.subject_id,self.teacher_id,self.room_id,
             self.time_slot_id,self.session_duration,int(self.is_locked))).lastrowid
    def delete(self):
        if self.id: db.execute("DELETE FROM schedule_entries WHERE id=?", (self.id,))
    @classmethod
    def delete_schedule(cls,sid): db.execute("DELETE FROM schedule_entries WHERE schedule_id=?", (sid,))

@dataclass
class LockedSession:
    id: Optional[int] = None; section_id: int = 0; subject_id: int = 0
    teacher_id: int = 0; room_id: int = 0; time_slot_id: int = 0; session_duration: int = 1
    @classmethod
    def all(cls): return [cls(**r) for r in db.query("SELECT * FROM locked_sessions")]
    def save(self):
        self.id=db.execute("INSERT INTO locked_sessions (section_id,subject_id,teacher_id,room_id,time_slot_id,session_duration) VALUES (?,?,?,?,?,?)",
            (self.section_id,self.subject_id,self.teacher_id,self.room_id,self.time_slot_id,self.session_duration)).lastrowid
    @classmethod
    def delete(cls,i): db.execute("DELETE FROM locked_sessions WHERE id=?", (i,))

@dataclass
class Absence:
    id: Optional[int] = None; teacher_id: int = 0; day: int = 1
    period_type: str = "morning"; substitute_teacher_id: Optional[int] = None; notes: str = ""
    @classmethod
    def all(cls): return [cls(**r) for r in db.query("SELECT * FROM absences ORDER BY created_at DESC")]
    def save(self):
        self.id=db.execute("INSERT INTO absences (teacher_id,day,period_type,substitute_teacher_id,notes) VALUES (?,?,?,?,?)",
            (self.teacher_id,self.day,self.period_type,self.substitute_teacher_id,self.notes)).lastrowid
    @classmethod
    def delete(cls,i): db.execute("DELETE FROM absences WHERE id=?", (i,))

def create_all_tables(): _ = db

def seed_demo_data():
    if Cycle.all(): return
    TimeSlot.initialize_default()
    inst = Institution.load(); inst.name = "متوسطة الأمل"; inst.year = "2024-2025"; inst.save()
    c = Cycle(name="الطور المتوسط"); c.save()
    levels = []
    for n in ["1 متوسط","2 متوسط","3 متوسط","4 متوسط"]:
        l = Level(cycle_id=c.id, name=n); l.save(); levels.append(l)
    rooms_data = [("قاعة M1","regular",35),("قاعة M2","regular",35),("قاعة M3","regular",35),
        ("قاعة M4","regular",35),("قاعة M5","regular",35),("قاعة M6","regular",35),
        ("قاعة M7","regular",35),("قاعة M8","regular",35),("قاعة M9","regular",35),("قاعة M10","regular",35),
        ("قاعة M11","regular",35),("قاعة M12","regular",35),("قاعة M13","regular",35),("قاعة M14","regular",35),
        ("قاعة M15","regular",35),("قاعة M16","regular",35),
        ("مخبر العلوم","science",30),("مخبر الفيزياء","physics",30),
        ("مخبر الإعلام الآلي","computer",25),("قاعة الرياضة","sport",60)]
    rooms = []
    for n,t,cap in rooms_data:
        r = Room(name=n,room_type=t,capacity=cap); r.save(); rooms.append(r)
    sections = []
    for i,lvl in enumerate(levels):
        for j,L in enumerate(["A","B","C","D"]):
            s = Section(level_id=lvl.id, name=f"{i+1}AM{L}", fixed_room_id=rooms[i*4+j].id)
            s.save(); sections.append(s)
    subjects_data = [("الرياضيات","#EF4444",None),("اللغة العربية","#3B82F6",None),
        ("اللغة الفرنسية","#8B5CF6",None),("اللغة الإنجليزية","#10B981",None),
        ("العلوم الطبيعية","#22C55E","science"),("العلوم الفيزيائية","#F97316","physics"),
        ("التاريخ والجغرافيا","#A855F7",None),("التربية الإسلامية","#06B6D4",None),
        ("التربية المدنية","#84CC16",None),("الإعلام الآلي","#0EA5E9","computer"),
        ("التربية البدنية","#F59E0B","sport"),("التربية التشكيلية","#EC4899",None)]
    subjects = []
    for n,col,rt in subjects_data:
        s = Subject(name=n,color=col,required_room_type=rt); s.save(); subjects.append(s)
    subj_dict = {s.name:s for s in subjects}
    for lvl in levels:
        for name,h in [("الرياضيات",5),("اللغة العربية",5),("اللغة الفرنسية",4),("اللغة الإنجليزية",3),
            ("العلوم الطبيعية",2),("العلوم الفيزيائية",2),("التاريخ والجغرافيا",2),
            ("التربية الإسلامية",2),("التربية المدنية",1),("الإعلام الآلي",1),
            ("التربية البدنية",2),("التربية التشكيلية",1)]:
            if name in subj_dict:
                SubjectHour(subject_id=subj_dict[name].id, level_id=lvl.id, hours_per_week=h).save()
    teachers_data = [
        ("أ. أحمد بن علي","الرياضيات",20,[0,1,2,3]),
        ("أ. فاطمة الزهراء","الرياضيات",20,[4,5,6,7]),
        ("أ. محمد بوزيد","الرياضيات",18,[8,9,10,11]),
        ("أ. سامية قاسمي","الرياضيات",18,[12,13,14,15]),
        ("أ. عبد الله حسين","اللغة العربية",20,[0,1,2,3]),
        ("أ. نادية مرابط","اللغة العربية",20,[4,5,6,7]),
        ("أ. خالد عماري","اللغة العربية",18,[8,9,10,11]),
        ("أ. مريم شريف","اللغة الفرنسية",20,[0,4,8,12]),
        ("أ. كمال عثماني","اللغة الفرنسية",20,[1,5,9,13]),
        ("أ. سارة مالكي","اللغة الإنجليزية",20,[0,4,8,12]),
        ("أ. عمر شريف","اللغة الإنجليزية",20,[1,5,9,13]),
        ("أ. رياض بلحاج","العلوم الطبيعية",16,[0,4,8,12]),
        ("أ. كمال عثماني (فيزياء)","العلوم الفيزيائية",16,[1,5,9,13]),
        ("أ. حسن زروقي","التاريخ والجغرافيا",18,[0,4,8,12]),
        ("أ. عبد الرحمن إمام","التربية الإسلامية",18,[0,4,8,12]),
        ("أ. ميلود حمدي","التربية المدنية",16, list(range(0,8))),
        ("أ. إبراهيم صحراوي","الإعلام الآلي",12,[0,4,8,12]),
        ("أ. حسام الدين","التربية البدنية",18, list(range(0,8))),
        ("أ. رابح فنان","التربية التشكيلية",16, list(range(0,8))),
    ]
    for full_name, subj_name, hours, sec_indices in teachers_data:
        if subj_name not in subj_dict: continue
        t = Teacher(full_name=full_name, subject_id=subj_dict[subj_name].id,
                    weekly_hours=hours, available_days="1,2,3,4,5", available_period="both",
                    section_ids=[sections[i].id for i in sec_indices])
        t.save()
    return True
