"""Warm theme for 研墨 Qt frontend."""

WARM_QSS = """
/* === 研墨 · Warm Theme === */

QMainWindow, QDialog, QWidget {
    background-color: #fdf6f0;
    color: #373a3c;
    font-family: "Noto Sans SC", "Microsoft YaHei", sans-serif;
    font-size: 14px;
}

QTabWidget::pane {
    border: 1px solid #e8e0d5;
    background: #fdf6f0;
}

QTabBar::tab {
    background: #fef8f3;
    color: #6b6e70;
    padding: 10px 22px;
    margin-right: 2px;
    border: none;
    border-bottom: 2px solid transparent;
    font-size: 13px;
}

QTabBar::tab:selected {
    color: #d97706;
    border-bottom: 2px solid #d97706;
    font-weight: bold;
    background: #fef3c7;
}

QTabBar::tab:hover:!selected {
    color: #373a3c;
    background: #fef0d5;
}

QPushButton {
    background-color: #d97706;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px 20px;
    font-size: 13px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #b45309;
}

QPushButton:pressed {
    background-color: #92400e;
}

QPushButton:disabled {
    background-color: #e8e0d5;
    color: #99968e;
}

QPushButton.secondary {
    background-color: transparent;
    color: #6b6e70;
    border: 1px solid #e8e0d5;
}

QPushButton.secondary:hover {
    color: #373a3c;
    border-color: #d97706;
}

QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, QSpinBox {
    border: 1px solid #e8e0d5;
    border-radius: 6px;
    padding: 8px 12px;
    background: white;
    color: #373a3c;
    font-size: 13px;
    selection-background-color: #fef3c7;
}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border-color: #f5d0a0;
}

QComboBox::drop-down {
    border: none;
    padding-right: 8px;
}

QComboBox QAbstractItemView {
    background: white;
    border: 1px solid #e8e0d5;
    selection-background-color: #fef3c7;
}

QGroupBox {
    border: 1px solid #e8e0d5;
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 16px;
    font-weight: 600;
    color: #373a3c;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
}

QScrollBar:vertical {
    border: none;
    background: transparent;
    width: 8px;
}

QScrollBar::handle:vertical {
    background: #e8e0d5;
    border-radius: 4px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background: #d0c8b8;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

QListWidget {
    border: 1px solid #e8e0d5;
    border-radius: 6px;
    background: white;
}

QListWidget::item {
    padding: 10px 14px;
    border-bottom: 1px solid #f0e8db;
}

QListWidget::item:hover {
    background: #fef8f3;
}

QListWidget::item:selected {
    background: #fef3c7;
    color: #373a3c;
}

QLabel.title {
    font-family: "Noto Serif SC", serif;
    font-size: 16px;
    font-weight: 700;
    color: #373a3c;
}

QLabel.subtitle {
    font-size: 12px;
    color: #99968e;
}

QSplitter::handle {
    background: #e8e0d5;
    width: 1px;
}

QStatusBar {
    background: #fef8f3;
    border-top: 1px solid #e8e0d5;
    color: #99968e;
    font-size: 11px;
}

QToolTip {
    background: #373a3c;
    color: #fdf6f0;
    border: none;
    border-radius: 4px;
    padding: 4px 8px;
}
"""

LIGHT_BUTTON = """
QPushButton {
    background-color: transparent;
    color: #6b6e70;
    border: 1px solid #e8e0d5;
    border-radius: 4px;
    padding: 4px 10px;
    font-size: 12px;
    font-weight: normal;
}
QPushButton:hover {
    color: #d97706;
    border-color: #d97706;
}
"""
