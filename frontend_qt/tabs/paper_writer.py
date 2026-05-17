"""写论文 — Qt tab."""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTextEdit, QPushButton, QLineEdit, QFrame,
)

from backend.plugins.paper_writer.outline import generate_outline
from backend.plugins.paper_writer.citation import parse_bibtex
from backend.plugins.paper_writer.deai import detect_ai_score, deai_text


class PaperWriterTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)

        # Outline section
        layout.addWidget(QLabel("大纲生成"))
        ot = QHBoxLayout()
        self.topic_input = QLineEdit()
        self.topic_input.setPlaceholderText("论文题目...")
        self.topic_input.returnPressed.connect(self._generate_outline)
        ot.addWidget(self.topic_input)
        outline_btn = QPushButton("生成大纲")
        outline_btn.clicked.connect(self._generate_outline)
        ot.addWidget(outline_btn)
        layout.addLayout(ot)

        self.outline_area = QVBoxLayout()
        layout.addLayout(self.outline_area)

        # Citation section
        layout.addWidget(QLabel("引文管理"))
        self.bibtex_input = QTextEdit()
        self.bibtex_input.setPlaceholderText("粘贴 BibTeX 条目...")
        self.bibtex_input.setMaximumHeight(100)
        self.bibtex_input.setStyleSheet("font-family: 'JetBrains Mono', monospace;")
        layout.addWidget(self.bibtex_input)
        parse_btn = QPushButton("解析")
        parse_btn.clicked.connect(self._parse_bibtex)
        layout.addWidget(parse_btn)
        self.citation_area = QVBoxLayout()
        layout.addLayout(self.citation_area)

        # De-AI section
        layout.addWidget(QLabel("去 AI 味"))
        self.deai_input = QTextEdit()
        self.deai_input.setPlaceholderText("粘贴文本，检测 AI 写作痕迹...")
        self.deai_input.setMaximumHeight(100)
        layout.addWidget(self.deai_input)

        dt = QHBoxLayout()
        deai_btn = QPushButton("检测 & 清洗")
        deai_btn.clicked.connect(self._run_deai)
        dt.addWidget(deai_btn)
        self.deai_score_label = QLabel()
        dt.addWidget(self.deai_score_label)
        dt.addStretch()
        layout.addLayout(dt)

        self.deai_result = QTextEdit()
        self.deai_result.setReadOnly(True)
        self.deai_result.setMaximumHeight(120)
        layout.addWidget(self.deai_result)

    def _generate_outline(self):
        topic = self.topic_input.text().strip()
        if not topic:
            return

        while self.outline_area.count():
            item = self.outline_area.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        sections = generate_outline(topic)
        total = sum(s.estimated_words for s in sections)
        self.outline_area.addWidget(
            QLabel(f"预计总字数: {total}")
        )

        for s in sections:
            card = QFrame()
            card.setStyleSheet(
                "background: #fffbf7; border: 1px solid #e8e0d5; "
                "border-radius: 6px; padding: 8px 12px; margin-bottom: 4px;"
            )
            cl = QVBoxLayout(card)
            hl = QHBoxLayout()
            hl.addWidget(QLabel(s.title))
            hl.addStretch()
            hl.addWidget(QLabel(f"~{s.estimated_words} 字"))
            cl.addLayout(hl)
            for kp in s.key_points:
                cl.addWidget(QLabel(f"· {kp}"))
            self.outline_area.addWidget(card)

    def _parse_bibtex(self):
        text = self.bibtex_input.toPlainText().strip()
        if not text:
            return

        while self.citation_area.count():
            item = self.citation_area.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        entries = parse_bibtex(text)
        self.citation_area.addWidget(QLabel(f"共 {len(entries)} 条引文"))
        for e in entries[:10]:
            self.citation_area.addWidget(
                QLabel(f"[{e.cite_key}] {e.title} — {e.author} ({e.year})")
            )

    def _run_deai(self):
        text = self.deai_input.toPlainText().strip()
        if not text:
            return

        score = detect_ai_score(text)
        cleaned = deai_text(text)
        cleaned_score = detect_ai_score(cleaned)

        self.deai_score_label.setText(
            f"AI 评分: {score['score']} → {cleaned_score['score']}"
        )
        self.deai_result.setText(cleaned)
