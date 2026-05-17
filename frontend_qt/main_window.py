"""Main window for 研墨 — native Qt frontend."""

from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QSplitter, QLabel, QStatusBar, QFrame,
)

from frontend_qt.widgets.theme import WARM_QSS
from frontend_qt.widgets.chat import ChatWidget
from frontend_qt.tabs.term_advisor import TermAdvisorTab
from frontend_qt.tabs.literature import LiteratureTab
from frontend_qt.tabs.evaluator import EvaluatorTab
from frontend_qt.tabs.formula import FormulaTab
from frontend_qt.tabs.paper_writer import PaperWriterTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("研墨")
        self.resize(1200, 800)
        self.setMinimumSize(900, 600)

        self.setStyleSheet(WARM_QSS)

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Header
        header = self._build_header()
        root.addWidget(header)

        # Tab widget + sidebar
        splitter = QSplitter(Qt.Orientation.Horizontal)
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)

        self.tabs.addTab(TermAdvisorTab(), "读懂导师")
        self.tabs.addTab(LiteratureTab(), "追新论文")
        self.tabs.addTab(EvaluatorTab(), "审项目")
        self.tabs.addTab(FormulaTab(), "验公式")
        self.tabs.addTab(PaperWriterTab(), "写论文")

        splitter.addWidget(self.tabs)

        # Sidebar
        sidebar = QWidget()
        sidebar.setFixedWidth(320)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        sidebar_layout.addWidget(ChatWidget())
        splitter.addWidget(sidebar)

        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 0)
        root.addWidget(splitter, 1)

        # Status bar
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("就绪")

    def _build_header(self) -> QFrame:
        frame = QFrame()
        frame.setFixedHeight(48)
        frame.setStyleSheet("background: #fffbf7; border-bottom: 1px solid #f0e8db;")
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(20, 0, 20, 0)

        title = QLabel("研墨")
        title.setStyleSheet(
            "font-family: 'Noto Serif SC', serif; font-size: 16px; font-weight: 700; color: #373a3c;"
        )
        layout.addWidget(title)

        hour = datetime.now().hour
        if hour < 7:
            msg = "夜深了，注意休息"
        elif hour < 12:
            msg = "早上好，今天也是充实的一天"
        elif hour < 14:
            msg = "中午好，别忘记吃午饭"
        elif hour < 18:
            msg = "下午好，来杯咖啡吧"
        else:
            msg = "晚上好，今天辛苦了"

        greeting = QLabel(msg)
        greeting.setStyleSheet("font-size: 12px; color: #99968e;")
        layout.addWidget(greeting)
        layout.addStretch()

        return frame
