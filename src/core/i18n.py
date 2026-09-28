# -*- coding: utf-8 -*-
"""نظام الترجمة - 3 لغات"""
import json
from pathlib import Path

_TRANSLATIONS_DIR = Path(__file__).parent / "translations"
_current_lang = "ar"
_translations = {}

DEFAULT_TRANSLATIONS = {
    "ar": {
        "app_title": "نظام إدارة الجداول المدرسية", "app_subtitle": "إنشاء وإدارة الجداول آليًا",
        "save": "حفظ", "cancel": "إلغاء", "delete": "حذف", "edit": "تعديل", "add": "إضافة",
        "new": "جديد", "search": "بحث", "close": "إغلاق", "ok": "موافق", "yes": "نعم", "no": "لا",
        "confirm": "تأكيد", "loading": "جارٍ التحميل...", "no_data": "لا توجد بيانات",
        "name": "الاسم", "actions": "إجراءات", "active": "نشط", "all": "الكل", "select": "اختر...",
        "required": "مطلوب", "nav_dashboard": "لوحة التحكم", "nav_institution": "المؤسسة",
        "nav_cycles": "الأطوار والمستويات", "nav_sections": "الأقسام", "nav_subjects": "المواد",
        "nav_teachers": "الأساتذة", "nav_rooms": "القاعات", "nav_time": "أوقات الدراسة",
        "nav_constraints": "القيود والإعدادات", "nav_generate": "إنشاء الجدول",
        "nav_view": "عرض الجداول", "nav_absences": "الغيابات", "nav_export": "طباعة وتصدير",
        "nav_help": "المساعدة", "institution_title": "بيانات المؤسسة",
        "institution_name": "اسم المؤسسة", "institution_year": "السنة الدراسية",
        "use_fixed_rooms": "تفعيل القاعات الثابتة", "distribute_subjects": "توزيع المواد على الأسبوع",
        "respect_teacher_hours": "احترام الحجم الساعي للأساتذة", "language": "لغة الواجهة",
        "day_1": "الأحد", "day_2": "الإثنين", "day_3": "الثلاثاء", "day_4": "الأربعاء", "day_5": "الخميس",
        "morning": "الفترة الصباحية", "evening": "الفترة المسائية", "both_periods": "الفترتان",
        "generate_btn": "🤖 إنشاء الجدول تلقائيًا", "generate_success": "تم إنشاء الجدول بنجاح!",
        "generate_failed": "تعذر إنشاء الجدول كاملًا", "schedule_metrics": "مؤشرات الجدول",
        "schedule_conflicts": "عدد التعارضات", "schedule_unassigned": "الحصص غير الموزعة",
        "schedule_score": "نقاط الجدول", "view_section": "جدول القسم", "view_teacher": "جدول الأستاذ",
        "view_room": "جدول القاعة", "view_export_excel": "📊 تصدير Excel", "view_print": "🖨️ طباعة",
        "msg_saved": "تم الحفظ بنجاح ✓", "msg_deleted": "تم الحذف ✓", "msg_confirm_delete": "هل أنت متأكد من الحذف؟",
        "msg_error": "خطأ: {error}", "load_demo": "📦 تحميل بيانات تجريبية", "demo_loaded": "تم تحميل البيانات التجريبية!",
        "constraints_hard": "القيود الصلبة (إلزامية)", "constraints_soft": "القيود المرنة (تحسين)",
        "file": "ملف", "exit": "خروج", "help": "مساعدة", "about": "حول البرنامج",
    },
    "fr": {
        "app_title": "Système de Gestion des Emplois du Temps", "save": "Enregistrer",
        "cancel": "Annuler", "delete": "Supprimer", "edit": "Modifier", "add": "Ajouter",
        "day_1": "Dimanche", "day_2": "Lundi", "day_3": "Mardi", "day_4": "Mercredi", "day_5": "Jeudi",
    },
    "en": {
        "app_title": "School Timetable Management System", "save": "Save",
        "cancel": "Cancel", "delete": "Delete", "edit": "Edit", "add": "Add",
        "day_1": "Sunday", "day_2": "Monday", "day_3": "Tuesday", "day_4": "Wednesday", "day_5": "Thursday",
    },
}

def save_default_translations():
    _TRANSLATIONS_DIR.mkdir(parents=True, exist_ok=True)
    for lang, data in DEFAULT_TRANSLATIONS.items():
        with open(_TRANSLATIONS_DIR / f"{lang}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    load_translations()

def load_translations():
    global _translations
    _translations = {}
    for lang_file in (_TRANSLATIONS_DIR or Path()).glob("*.json") if _TRANSLATIONS_DIR.exists() else []:
        try:
            with open(lang_file, "r", encoding="utf-8") as f:
                _translations[lang_file.stem] = json.load(f)
        except Exception: _translations[lang_file.stem] = {}

def set_language(lang):
    global _current_lang
    if not _translations: load_translations()
    _current_lang = lang if lang in _translations else "ar"

def get_language(): return _current_lang

def is_rtl(): return _current_lang in ("ar", "he", "fa")

def tr(key, **kwargs):
    if not _translations: load_translations()
    text = _translations.get(_current_lang, {}).get(key)
    if text is None: text = _translations.get("ar", {}).get(key, key)
    if kwargs:
        try: text = text.format(**kwargs)
        except Exception: pass
    return text

save_default_translations()
