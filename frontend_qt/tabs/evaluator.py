"""审项目 — Qt tab."""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QTextEdit, QPushButton, QFrame,
)

from backend.plugins.evaluator.evaluate import evaluate_project


class EvaluatorTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("项目名称")
        layout.addWidget(self.title_input)

        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("项目描述（研究问题、方法、创新点、预期成果等）")
        self.desc_input.setMaximumHeight(160)
        layout.addWidget(self.desc_input)

        self.run_btn = QPushButton("开始评估")
        self.run_btn.clicked.connect(self._evaluate)
        layout.addWidget(self.run_btn)

        self.result_area = QVBoxLayout()
        layout.addLayout(self.result_area)
        layout.addStretch()

    def _evaluate(self):
        title = self.title_input.text().strip()
        desc = self.desc_input.toPlainText().strip()
        if not desc:
            return

        result = evaluate_project(title, desc)

        # Clear old results
        while self.result_area.count():
            item = self.result_area.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Scores
        scores_frame = QFrame()
        scores_frame.setStyleSheet(
            "background: #fffbf7; border: 1px solid #e8e0d5; border-radius: 8px; padding: 12px;"
        )
        sl = QHBoxLayout(scores_frame)
        for label, score, color in [
            ("创新性", result.innovation_score, "#d97706"),
            ("合理性", result.rationality_score, "#65a30d"),
            ("方法论", result.methodology_score, "#8b5cf6"),
        ]:
            box = QFrame()
            bl = QVBoxLayout(box)
            score_lbl = QLabel(str(score))
            score_lbl.setStyleSheet(
                f"font-size: 28px; font-weight: 700; color: {color};"
            )
            label_lbl = QLabel(f"/10 {label}")
            label_lbl.setStyleSheet("font-size: 12px; color: #99968e;")
            bl.addWidget(score_lbl)
            bl.addWidget(label_lbl)
            sl.addWidget(box)
        self.result_area.addWidget(scores_frame)

        # Details
        for title, items, color in [
            ("优势", result.strengths, "#65a30d"),
            ("不足", result.weaknesses, "#dc2626"),
            ("建议", result.suggestions, "#d97706"),
        ]:
            if items:
                section = QFrame()
                sl = QVBoxLayout(section)
                lbl = QLabel(title)
                lbl.setStyleSheet(f"font-weight: 600; color: {color};")
                sl.addWidget(lbl)
                for item in items:
                    sl.addWidget(QLabel(f"· {item}"))
                self.result_area.addWidget(section)
