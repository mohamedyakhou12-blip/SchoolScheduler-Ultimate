# -*- coding: utf-8 -*-
"""نظام الترجمة - 3 لغات كاملة"""
import json
from pathlib import Path

_TRANSLATIONS_DIR = Path(__file__).parent / "translations"
_current_lang = "ar"
_translations = {}

# الترجمات الكاملة للغات الثلاث
TRANSLATIONS = {
    "ar": {
        "app_title": "نظام إدارة الجداول المدرسية", "app_subtitle": "إنشاء وإدارة الجداول آليًا",
        "save": "حفظ", "cancel": "إلغاء", "delete": "حذف", "edit": "تعديل", "add": "إضافة",
        "new": "جديد", "search": "بحث", "close": "إغلاق", "ok": "موافق", "yes": "نعم", "no": "لا",
        "confirm": "تأكيد", "loading": "جارٍ التحميل...", "no_data": "لا توجد بيانات",
        "name": "الاسم", "actions": "إجراءات", "active": "نشط", "all": "الكل", "select": "اختر...",
        "required": "مطلوب",
        "nav_dashboard": "لوحة التحكم", "nav_institution": "المؤسسة",
        "nav_cycles": "الأطوار والمستويات", "nav_sections": "الأقسام", "nav_subjects": "المواد",
        "nav_teachers": "الأساتذة", "nav_rooms": "القاعات", "nav_time": "أوقات الدراسة",
        "nav_constraints": "القيود والإعدادات", "nav_generate": "إنشاء الجدول",
        "nav_view": "عرض الجداول", "nav_absences": "الغيابات", "nav_export": "طباعة وتصدير",
        "nav_help": "المساعدة",
        "institution_title": "بيانات المؤسسة", "institution_name": "اسم المؤسسة",
        "institution_year": "السنة الدراسية",
        "use_fixed_rooms": "تفعيل القاعات الثابتة", "allow_free_periods": "السماح بالفراغات",
        "distribute_subjects": "توزيع المواد على الأسبوع",
        "respect_teacher_hours": "احترام الحجم الساعي للأساتذة", "language": "لغة الواجهة",
        "day_1": "الأحد", "day_2": "الإثنين", "day_3": "الثلاثاء", "day_4": "الأربعاء", "day_5": "الخميس",
        "morning": "الفترة الصباحية", "evening": "الفترة المسائية", "both_periods": "الفترتان",
        "generate_btn": "🤖 إنشاء الجدول تلقائيًا", "generate_success": "تم إنشاء الجدول بنجاح!",
        "generate_failed": "تعذر إنشاء الجدول كاملًا", "schedule_metrics": "مؤشرات الجدول",
        "schedule_conflicts": "عدد التعارضات", "schedule_unassigned": "الحصص غير الموزعة",
        "schedule_score": "نقاط الجدول", "schedule_active": "الجدول النشط",
        "view_section": "جدول القسم", "view_teacher": "جدول الأستاذ",
        "view_room": "جدول القاعة", "view_export_excel": "📊 تصدير Excel",
        "view_export_pdf": "📄 تصدير PDF", "view_print": "🖨️ طباعة",
        "msg_saved": "تم الحفظ بنجاح ✓", "msg_deleted": "تم الحذف ✓",
        "msg_confirm_delete": "هل أنت متأكد من الحذف؟", "msg_error": "خطأ: {error}",
        "msg_required_field": "هذا الحقل مطلوب",
        "load_demo": "📦 تحميل بيانات تجريبية", "demo_loaded": "تم تحميل البيانات التجريبية!",
        "constraints_hard": "القيود الصلبة (إلزامية)", "constraints_soft": "القيود المرنة (تحسين)",
        "file": "ملف", "exit": "خروج", "help": "مساعدة", "about": "حول البرنامج",
        "subject_name": "اسم المادة", "subject_color": "اللون", "required_room_type": "القاعة المطلوبة",
        "teacher_name": "الاسم الكامل", "teacher_subject": "المادة", "teacher_hours": "الحجم الساعي",
        "teacher_sections": "الأقسام", "teacher_available_days": "الأيام المتاحة",
        "teacher_available_period": "الفترة المتاحة",
        "room_name": "اسم القاعة", "room_type": "النوع", "capacity": "السعة",
        "regular": "قاعة عادية", "science": "مخبر العلوم", "physics": "مخبر الفيزياء",
        "computer": "مخبر الإعلام الآلي", "sport": "قاعة الرياضة", "other": "أخرى",
        "section_name": "اسم القسم", "section_level": "المستوى", "fixed_room": "القاعة الثابتة",
        "no_fixed_room": "بدون قاعة ثابتة",
        "cycle_name": "اسم الطور", "level_name": "اسم المستوى",
        "cycles": "الأطوار", "levels": "المستويات", "add_cycle": "إضافة طور",
        "add_level": "إضافة مستوى", "add_section": "إضافة قسم", "add_subject": "إضافة مادة",
        "add_teacher": "إضافة أستاذ", "add_room": "إضافة قاعة",
        "time_slots": "الحصص", "time_morning_period": "الفترة الصباحية (08:00 - 12:00)",
        "time_evening_period": "الفترة المسائية (13:30 - 16:30)",
        "time_reset_default": "إعادة تعيين الحصص الافتراضية",
        "manage_hours": "إدارة ساعات المواد", "weekly_hours": "الساعات الأسبوعية",
        "add_absence": "تسجيل غياب", "absent_teacher": "الأستاذ الغائب",
        "absence_day": "اليوم", "absence_period": "الفترة",
        "substitute": "الأستاذ البديل", "find_substitute": "بحث عن بديل",
        "view_lock": "🔒 قفل الحصة", "view_unlock": "🔓 فك القفل",
        "view_delete_entry": "🗑️ حذف الحصة", "view_no_active_schedule": "لا يوجد جدول نشط",
        "no_schedules": "لا توجد جداول محفوظة",
    },
    "fr": {
        "app_title": "Système de Gestion des Emplois du Temps", "app_subtitle": "Création et gestion automatiques",
        "save": "Enregistrer", "cancel": "Annuler", "delete": "Supprimer", "edit": "Modifier", "add": "Ajouter",
        "new": "Nouveau", "search": "Rechercher", "close": "Fermer", "ok": "OK", "yes": "Oui", "no": "Non",
        "confirm": "Confirmer", "loading": "Chargement...", "no_data": "Aucune donnée",
        "name": "Nom", "actions": "Actions", "active": "Actif", "all": "Tous", "select": "Choisir...",
        "required": "Requis",
        "nav_dashboard": "Tableau de bord", "nav_institution": "Établissement",
        "nav_cycles": "Cycles & Niveaux", "nav_sections": "Classes", "nav_subjects": "Matières",
        "nav_teachers": "Enseignants", "nav_rooms": "Salles", "nav_time": "Horaires",
        "nav_constraints": "Contraintes", "nav_generate": "Générer l'emploi",
        "nav_view": "Voir les emplois", "nav_absences": "Absences", "nav_export": "Imprimer & Exporter",
        "nav_help": "Aide",
        "institution_title": "Données de l'établissement", "institution_name": "Nom de l'établissement",
        "institution_year": "Année scolaire",
        "use_fixed_rooms": "Activer les salles fixes", "allow_free_periods": "Autoriser les trous",
        "distribute_subjects": "Répartir les matières sur la semaine",
        "respect_teacher_hours": "Respecter le volume horaire des enseignants", "language": "Langue",
        "day_1": "Dimanche", "day_2": "Lundi", "day_3": "Mardi", "day_4": "Mercredi", "day_5": "Jeudi",
        "morning": "Matin", "evening": "Après-midi", "both_periods": "Les deux",
        "generate_btn": "🤖 Générer l'emploi du temps", "generate_success": "Emploi créé avec succès!",
        "generate_failed": "Impossible de créer l'emploi complet", "schedule_metrics": "Indicateurs",
        "schedule_conflicts": "Conflits", "schedule_unassigned": "Séances non assignées",
        "schedule_score": "Score", "schedule_active": "Emploi actif",
        "view_section": "Emploi de la classe", "view_teacher": "Emploi de l'enseignant",
        "view_room": "Emploi de la salle", "view_export_excel": "📊 Exporter Excel",
        "view_export_pdf": "📄 Exporter PDF", "view_print": "🖨️ Imprimer",
        "msg_saved": "Enregistré ✓", "msg_deleted": "Supprimé ✓",
        "msg_confirm_delete": "Confirmer la suppression?", "msg_error": "Erreur: {error}",
        "msg_required_field": "Champ requis",
        "load_demo": "📦 Charger données démo", "demo_loaded": "Données démo chargées!",
        "constraints_hard": "Contraintes dures", "constraints_soft": "Contraintes souples",
        "file": "Fichier", "exit": "Quitter", "help": "Aide", "about": "À propos",
        "subject_name": "Matière", "subject_color": "Couleur", "required_room_type": "Salle requise",
        "teacher_name": "Nom complet", "teacher_subject": "Matière", "teacher_hours": "Volume horaire",
        "teacher_sections": "Classes", "teacher_available_days": "Jours disponibles",
        "teacher_available_period": "Période disponible",
        "room_name": "Salle", "room_type": "Type", "capacity": "Capacité",
        "regular": "Salle ordinaire", "science": "Labo Sciences", "physics": "Labo Physique",
        "computer": "Labo Informatique", "sport": "Salle de Sport", "other": "Autre",
        "section_name": "Classe", "section_level": "Niveau", "fixed_room": "Salle fixe",
        "no_fixed_room": "Sans salle fixe",
        "cycle_name": "Cycle", "level_name": "Niveau",
        "cycles": "Cycles", "levels": "Niveaux", "add_cycle": "Ajouter cycle",
        "add_level": "Ajouter niveau", "add_section": "Ajouter classe", "add_subject": "Ajouter matière",
        "add_teacher": "Ajouter enseignant", "add_room": "Ajouter salle",
        "time_slots": "Séances", "time_morning_period": "Matin (08:00 - 12:00)",
        "time_evening_period": "Après-midi (13:30 - 16:30)",
        "time_reset_default": "Réinitialiser horaires",
        "manage_hours": "Gérer les heures", "weekly_hours": "Heures hebdomadaires",
        "add_absence": "Enregistrer absence", "absent_teacher": "Enseignant absent",
        "absence_day": "Jour", "absence_period": "Période",
        "substitute": "Enseignant remplaçant", "find_substitute": "Chercher remplaçant",
        "view_lock": "🔒 Verrouiller", "view_unlock": "🔓 Déverrouiller",
        "view_delete_entry": "🗑️ Supprimer", "view_no_active_schedule": "Aucun emploi actif",
        "no_schedules": "Aucun emploi enregistré",
    },
    "en": {
        "app_title": "School Timetable Management System", "app_subtitle": "Automatic timetable creation and management",
        "save": "Save", "cancel": "Cancel", "delete": "Delete", "edit": "Edit", "add": "Add",
        "new": "New", "search": "Search", "close": "Close", "ok": "OK", "yes": "Yes", "no": "No",
        "confirm": "Confirm", "loading": "Loading...", "no_data": "No data",
        "name": "Name", "actions": "Actions", "active": "Active", "all": "All", "select": "Select...",
        "required": "Required",
        "nav_dashboard": "Dashboard", "nav_institution": "Institution",
        "nav_cycles": "Cycles & Levels", "nav_sections": "Sections", "nav_subjects": "Subjects",
        "nav_teachers": "Teachers", "nav_rooms": "Rooms", "nav_time": "Time Slots",
        "nav_constraints": "Constraints", "nav_generate": "Generate Schedule",
        "nav_view": "View Schedules", "nav_absences": "Absences", "nav_export": "Print & Export",
        "nav_help": "Help",
        "institution_title": "Institution Data", "institution_name": "Institution Name",
        "institution_year": "School Year",
        "use_fixed_rooms": "Enable Fixed Rooms", "allow_free_periods": "Allow Free Periods",
        "distribute_subjects": "Distribute Subjects Across Week",
        "respect_teacher_hours": "Respect Teacher Weekly Hours", "language": "Language",
        "day_1": "Sunday", "day_2": "Monday", "day_3": "Tuesday", "day_4": "Wednesday", "day_5": "Thursday",
        "morning": "Morning", "evening": "Afternoon", "both_periods": "Both",
        "generate_btn": "🤖 Generate Timetable Automatically", "generate_success": "Schedule created successfully!",
        "generate_failed": "Could not create complete schedule", "schedule_metrics": "Schedule Metrics",
        "schedule_conflicts": "Conflicts", "schedule_unassigned": "Unassigned Sessions",
        "schedule_score": "Score", "schedule_active": "Active Schedule",
        "view_section": "Section Schedule", "view_teacher": "Teacher Schedule",
        "view_room": "Room Schedule", "view_export_excel": "📊 Export Excel",
        "view_export_pdf": "📄 Export PDF", "view_print": "🖨️ Print",
        "msg_saved": "Saved successfully ✓", "msg_deleted": "Deleted ✓",
        "msg_confirm_delete": "Are you sure you want to delete?", "msg_error": "Error: {error}",
        "msg_required_field": "This field is required",
        "load_demo": "📦 Load Demo Data", "demo_loaded": "Demo data loaded successfully!",
        "constraints_hard": "Hard Constraints (Mandatory)", "constraints_soft": "Soft Constraints (Optimization)",
        "file": "File", "exit": "Exit", "help": "Help", "about": "About",
        "subject_name": "Subject Name", "subject_color": "Color", "required_room_type": "Required Room Type",
        "teacher_name": "Full Name", "teacher_subject": "Subject", "teacher_hours": "Weekly Hours",
        "teacher_sections": "Sections", "teacher_available_days": "Available Days",
        "teacher_available_period": "Available Period",
        "room_name": "Room Name", "room_type": "Type", "capacity": "Capacity",
        "regular": "Regular Room", "science": "Science Lab", "physics": "Physics Lab",
        "computer": "Computer Lab", "sport": "Sports Hall", "other": "Other",
        "section_name": "Section Name", "section_level": "Level", "fixed_room": "Fixed Room",
        "no_fixed_room": "No Fixed Room",
        "cycle_name": "Cycle", "level_name": "Level",
        "cycles": "Cycles", "levels": "Levels", "add_cycle": "Add Cycle",
        "add_level": "Add Level", "add_section": "Add Section", "add_subject": "Add Subject",
        "add_teacher": "Add Teacher", "add_room": "Add Room",
        "time_slots": "Time Slots", "time_morning_period": "Morning (08:00 - 12:00)",
        "time_evening_period": "Afternoon (13:30 - 16:30)",
        "time_reset_default": "Reset Default Slots",
        "manage_hours": "Manage Hours", "weekly_hours": "Weekly Hours",
        "add_absence": "Record Absence", "absent_teacher": "Absent Teacher",
        "absence_day": "Day", "absence_period": "Period",
        "substitute": "Substitute Teacher", "find_substitute": "Find Substitute",
        "view_lock": "🔒 Lock Session", "view_unlock": "🔓 Unlock",
        "view_delete_entry": "🗑️ Delete Session", "view_no_active_schedule": "No active schedule",
        "no_schedules": "No saved schedules",
    },
}

def save_translations():
    """حفظ ملفات الترجمة"""
    _TRANSLATIONS_DIR.mkdir(parents=True, exist_ok=True)
    for lang, data in TRANSLATIONS.items():
        with open(_TRANSLATIONS_DIR / f"{lang}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    load_translations()

def load_translations():
    """تحميل ملفات الترجمة"""
    global _translations
    _translations = {}
    if not _TRANSLATIONS_DIR.exists():
        _TRANSLATIONS_DIR.mkdir(parents=True, exist_ok=True)
    for lang_file in _TRANSLATIONS_DIR.glob("*.json"):
        try:
            with open(lang_file, "r", encoding="utf-8") as f:
                _translations[lang_file.stem] = json.load(f)
        except Exception:
            _translations[lang_file.stem] = {}
    # إذا لم توجد، استخدم الافتراضية
    if not _translations:
        _translations = TRANSLATIONS.copy()

def set_language(lang):
    """تغيير اللغة"""
    global _current_lang
    if not _translations:
        load_translations()
    if lang in _translations:
        _current_lang = lang
    else:
        _current_lang = "ar"

def get_language():
    return _current_lang

def is_rtl():
    return _current_lang in ("ar", "he", "fa")

def tr(key, **kwargs):
    """ترجمة مفتاح"""
    if not _translations:
        load_translations()
    text = _translations.get(_current_lang, {}).get(key)
    if text is None:
        text = _translations.get("ar", {}).get(key, key)
    if kwargs:
        try:
            text = text.format(**kwargs)
        except Exception:
            pass
    return text

def get_available_languages():
    """إرجاع اللغات المتاحة"""
    return list(TRANSLATIONS.keys())

# التهيئة عند الاستيراد
save_translations()
