# -*- coding: utf-8 -*-
"""تنسيقات احترافية v7.0"""

APP_STYLESHEET = """
QWidget { background-color: #0F172A; color: #E2E8F0;
    font-family: 'Tahoma', 'Noto Sans Arabic', 'Cairo', 'Segoe UI', 'DejaVu Sans', 'Arial'; font-size: 13px; }
QMainWindow { background-color: #0F172A; }
#Sidebar { background-color: #1E293B; border-left: 1px solid #334155; min-width: 250px; max-width: 270px; }
QLabel#sidebarTitle { color: #F1F5F9; font-size: 17px; font-weight: bold; padding: 20px 20px 8px 20px; background: transparent; }
QLabel#sidebarSubtitle { color: #94A3B8; font-size: 11px; padding: 0 20px 16px 20px; background: transparent; }
QPushButton#navButton { background: transparent; color: #CBD5E1; text-align: left; padding: 14px 20px;
    border: none; font-size: 14px; min-height: 44px; }
QPushButton#navButton:hover { background-color: rgba(59,130,246,0.1); color: #F1F5F9; border-left: 3px solid #3B82F6; }
QPushButton#navButton:checked { background-color: rgba(59,130,246,0.15); color: #3B82F6; border-left: 3px solid #3B82F6; font-weight: bold; }
QPushButton#navButtonPrimary { background-color: #3B82F6; color: white; border: none; padding: 12px; border-radius: 8px; font-weight: bold; font-size: 13px; margin: 12px 16px; }
QPushButton#navButtonPrimary:hover { background-color: #2563EB; }
QLabel#pageTitle { color: #F1F5F9; font-size: 26px; font-weight: bold; padding: 8px 0; }
QLabel#pageSubtitle { color: #94A3B8; font-size: 13px; padding-bottom: 16px; }
QFrame#card { background-color: #1E293B; border-radius: 12px; border: 1px solid #334155; }
QLabel#cardTitle { color: #F1F5F9; font-size: 16px; font-weight: bold; }
QLineEdit, QSpinBox, QComboBox, QDoubleSpinBox, QTextEdit { background-color: #0F172A; color: #E2E8F0;
    border: 1.5px solid #334155; border-radius: 8px; padding: 10px 14px; font-size: 13px; selection-background-color: #3B82F6; }
QLineEdit:focus, QSpinBox:focus, QComboBox:focus, QTextEdit:focus { border: 1.5px solid #3B82F6; background-color: #1A2540; }
QComboBox::drop-down { border: none; width: 32px; }
QComboBox::down-arrow { border-left: 5px solid transparent; border-right: 5px solid transparent; border-top: 6px solid #94A3B8; margin-right: 10px; }
QComboBox QAbstractItemView { background-color: #1E293B; color: #E2E8F0; border: 1.5px solid #334155; border-radius: 8px; selection-background-color: #3B82F6; }
QPushButton { background-color: #334155; color: #E2E8F0; border: none; border-radius: 8px; padding: 10px 18px; font-size: 13px; font-weight: 500; }
QPushButton:hover { background-color: #475569; }
QPushButton:pressed { background-color: #1F2937; }
QPushButton:disabled { background-color: #1E293B; color: #475569; }
QPushButton#primaryButton { background-color: #3B82F6; color: white; font-weight: bold; padding: 11px 22px; border-radius: 8px; }
QPushButton#primaryButton:hover { background-color: #2563EB; }
QPushButton#dangerButton { background-color: #DC2626; color: white; font-weight: bold; border-radius: 8px; }
QPushButton#dangerButton:hover { background-color: #B91C1C; }
QTableWidget { background-color: #1E293B; alternate-background-color: #1A2540; border: 1px solid #334155; border-radius: 8px;
    gridline-color: #334155; selection-background-color: #3B82F6; }
QTableWidget::item { padding: 10px; color: #E2E8F0; }
QHeaderView::section { background-color: #0F172A; color: #F1F5F9; padding: 12px; border: none;
    border-right: 1px solid #334155; border-bottom: 2px solid #3B82F6; font-weight: bold; }
QTabWidget::pane { background-color: #0F172A; border: 1px solid #334155; border-radius: 8px; }
QTabBar::tab { background-color: #1E293B; color: #94A3B8; padding: 12px 26px; border: 1px solid #334155;
    border-bottom: none; border-top-left-radius: 8px; border-top-right-radius: 8px; margin-right: 4px; }
QTabBar::tab:selected { background-color: #0F172A; color: #3B82F6; border-bottom: 2px solid #3B82F6; font-weight: bold; }
QCheckBox { color: #E2E8F0; spacing: 10px; padding: 6px; }
QCheckBox::indicator { width: 20px; height: 20px; border-radius: 6px; border: 1.5px solid #475569; background-color: #0F172A; }
QCheckBox::indicator:checked { background-color: #3B82F6; border: 1.5px solid #3B82F6; }
QScrollBar:vertical { background-color: #1E293B; width: 12px; border: none; border-radius: 6px; }
QScrollBar::handle:vertical { background-color: #475569; border-radius: 6px; min-height: 40px; margin: 2px; }
QScrollBar::handle:vertical:hover { background-color: #3B82F6; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QMenuBar { background-color: #1E293B; color: #E2E8F0; border-bottom: 1px solid #334155; padding: 4px; }
QMenuBar::item:selected { background-color: #334155; }
QMenu { background-color: #1E293B; color: #E2E8F0; border: 1px solid #334155; border-radius: 8px; padding: 4px; }
QMenu::item { padding: 8px 24px; border-radius: 6px; }
QMenu::item:selected { background-color: #3B82F6; color: white; }
QStatusBar { background-color: #1E293B; color: #94A3B8; border-top: 1px solid #334155; }
QToolTip { background-color: #1E293B; color: #E2E8F0; border: 1px solid #475569; border-radius: 6px; padding: 6px 10px; }
QListWidget { background-color: #1E293B; border: 1px solid #334155; border-radius: 8px; color: #E2E8F0; padding: 4px; }
QListWidget::item { padding: 10px 14px; border-bottom: 1px solid #334155; border-radius: 6px; }
QListWidget::item:selected { background-color: #3B82F6; color: white; }
"""
