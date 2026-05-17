"""读懂导师 — Qt tab."""

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton,
    QLabel, QScrollArea, QFrame, QComboBox,
)

from backend.plugins.term_advisor.advisor import parse_advisor_text, create_plan


class ParseThread(QThread):
    done = Signal(object)

    def __init__(self, text: str, mode: str):
        super().__init__()
        self.text = text
        self.mode = mode

    def run(self):
        tasks = parse_advisor_text(self.text)
        if self.mode == "plan":
            plan = create_plan(tasks)
            self.done.emit(("plan", plan))
        else:
            self.done.emit(("parse", tasks))


class TermAdvisorTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)

        # Security notice
        notice = QLabel(
            "本地模型处理，数据标记为机密，不会发送到任何云端服务"
        )
        notice.setStyleSheet(
            "background: #fef2f2; border: 1px solid #fecaca; border-radius: 8px; "
            "padding: 12px; font-size: 12px; color: #dc2626;"
        )
        notice.setWordWrap(True)
        layout.addWidget(notice)

        # Input
        self.input = QTextEdit()
        self.input.setPlaceholderText(
            "粘贴导师的原话...\n\n例如：先对 Transformer 做文献综述，然后实现一个改进的注意力机制，最后做实验对比基线"
        )
        self.input.setMaximumHeight(140)
        layout.addWidget(self.input)

        # Controls
        controls = QHBoxLayout()
        self.mode = QComboBox()
        self.mode.addItems(["Full Plan (生成完整计划)", "Parse Only (仅拆解任务)"])
        controls.addWidget(self.mode)

        self.run_btn = QPushButton("开始")
        self.run_btn.clicked.connect(self._run)
        controls.addWidget(self.run_btn)
        controls.addStretch()
        layout.addLayout(controls)

        # Results area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.result_widget = QWidget()
        self.result_layout = QVBoxLayout(self.result_widget)
        self.result_layout.addStretch()
        self.scroll.setWidget(self.result_widget)
        layout.addWidget(self.scroll, 1)

        self._thread = None

    def _run(self):
        text = self.input.toPlainText().strip()
        if not text:
            return
        self.run_btn.setEnabled(False)
        self.run_btn.setText("处理中...")
        mode = "plan" if self.mode.currentIndex() == 0 else "parse"

        # Clear results
        while self.result_layout.count() > 1:
            item = self.result_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self._thread = ParseThread(text, mode)
        self._thread.done.connect(self._show_result)
        self._thread.start()

    def _show_result(self, data):
        mode, result = data
        self.run_btn.setEnabled(True)
        self.run_btn.setText("开始")

        if mode == "parse":
            self._show_parse(result)
        else:
            self._show_plan(result)

    def _show_parse(self, tasks):
        label = QLabel(f"解析出 {len(tasks)} 个任务")
        label.setStyleSheet("font-weight: 600; font-size: 15px; margin-bottom: 8px;")
        self.result_layout.insertWidget(self.result_layout.count() - 1, label)

        for t in tasks:
            card = QFrame()
            card.setStyleSheet(
                "background: #fffbf7; border: 1px solid #e8e0d5; "
                "border-radius: 8px; padding: 12px; margin-bottom: 6px;"
            )
            cl = QVBoxLayout(card)
            action = QLabel(t.action)
            action.setStyleSheet("font-weight: 600;")
            cl.addWidget(action)

            if t.keywords:
                kw_text = "  ".join(t.keywords[:5])
                kw = QLabel(kw_text)
                kw.setStyleSheet("font-size: 12px; color: #d97706;")
                kw.setWordWrap(True)
                cl.addWidget(kw)

            self.result_layout.insertWidget(self.result_layout.count() - 1, card)

    def _show_plan(self, plan):
        # Summary
        summary = QFrame()
        summary.setStyleSheet("background: #fef3c7; border-radius: 8px; padding: 12px; margin-bottom: 12px;")
        sl = QHBoxLayout(summary)
        for text, val in [
            (f"{plan.total_days_min}–{plan.total_days_max} 天", "预估时间"),
            (f"{len(plan.tasks)} 个阶段", "任务数"),
        ]:
            box = QFrame()
            bl = QVBoxLayout(box)
            val_lbl = QLabel(val)
            val_lbl.setStyleSheet("font-size: 12px; color: #99968e;")
            text_lbl = QLabel(text)
            text_lbl.setStyleSheet("font-size: 20px; font-weight: 700; color: #d97706;")
            bl.addWidget(text_lbl)
            bl.addWidget(val_lbl)
            sl.addWidget(box)
        sl.addStretch()
        self.result_layout.insertWidget(self.result_layout.count() - 1, summary)

        # Tasks
        for task in plan.tasks:
            card = QFrame()
            card.setStyleSheet(
                "background: #fffbf7; border: 1px solid #e8e0d5; border-left: 3px solid #d97706; "
                "border-radius: 8px; padding: 12px; margin-bottom: 8px;"
            )
            cl = QVBoxLayout(card)

            header = QHBoxLayout()
            title = QLabel(f"{task.action}")
            title.setStyleSheet("font-weight: 700; font-size: 15px;")
            header.addWidget(title)
            header.addStretch()
            days = QLabel(f"{task.estimated_days_min}–{task.estimated_days_max} 天")
            days.setStyleSheet("font-size: 12px; color: #d97706; font-weight: 600;")
            header.addWidget(days)
            cl.addLayout(header)

            if task.subtasks:
                subs = QLabel("\n".join(f"· {s}" for s in task.subtasks[:5]))
                subs.setStyleSheet("font-size: 12px; color: #6b6e70;")
                subs.setWordWrap(True)
                cl.addWidget(subs)

            self.result_layout.insertWidget(self.result_layout.count() - 1, card)
