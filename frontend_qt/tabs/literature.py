"""追新论文 — Qt tab."""

import asyncio
import json

from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit,
    QLabel, QScrollArea, QFrame, QListWidget, QListWidgetItem,
    QTextEdit,
)

from backend.plugins.literature.crawlers import CrawlerManager
from backend.plugins.literature.crawlers.arxiv import ArxivCrawler
from backend.plugins.literature.crawlers.semantic_scholar import SemanticScholarCrawler
from backend.plugins.literature.crawlers.dblp import DBLPCrawler
from backend.plugins.literature.dedup import deduplicate
from backend.plugins.evaluator.gap_analyzer import analyze_gaps

_manager = CrawlerManager()
_manager.register(ArxivCrawler())
_manager.register(SemanticScholarCrawler())
_manager.register(DBLPCrawler())


class FeedThread(QThread):
    done = Signal(list, list)

    def __init__(self, keywords: list[str]):
        super().__init__()
        self.keywords = keywords

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            all_papers = []
            errors = []
            for kw in (self.keywords or ["machine learning"])[:3]:
                result = loop.run_until_complete(_manager.search_all(kw, max_results=8))
                all_papers.extend(result.papers)
                errors.extend(result.errors)
            deduped = deduplicate(all_papers)
            deduped.sort(key=lambda p: p.get("published", ""), reverse=True)
            self.done.emit(deduped[:20], errors[:5])
        finally:
            loop.close()


class GapThread(QThread):
    done = Signal(list)

    def __init__(self, papers):
        super().__init__()
        self.papers = papers

    def run(self):
        gaps = analyze_gaps(self.papers[:10])
        self.done.emit(gaps)


class LiteratureTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)

        # Interests
        self.interests: list[str] = []
        self.interest_tags = QHBoxLayout()
        layout.addLayout(self.interest_tags)

        interest_input = QHBoxLayout()
        self.interest_input = QLineEdit()
        self.interest_input.setPlaceholderText("添加关键词...")
        self.interest_input.returnPressed.connect(self._add_interest)
        interest_input.addWidget(self.interest_input)
        add_btn = QPushButton("+")
        add_btn.setFixedWidth(36)
        add_btn.clicked.connect(self._add_interest)
        interest_input.addWidget(add_btn)
        layout.addLayout(interest_input)

        # Buttons
        btns = QHBoxLayout()
        self.feed_btn = QPushButton("刷新 Feed")
        self.feed_btn.clicked.connect(self._load_feed)
        btns.addWidget(self.feed_btn)

        self.gap_btn = QPushButton("找思路")
        self.gap_btn.setProperty("class", "secondary")
        self.gap_btn.clicked.connect(self._find_gaps)
        btns.addWidget(self.gap_btn)

        btns.addStretch()
        layout.addLayout(btns)

        # Paper list
        self.paper_list = QListWidget()
        self.paper_list.setAlternatingRowColors(False)
        self.paper_list.currentRowChanged.connect(self._show_paper_detail)
        layout.addWidget(self.paper_list, 1)

        # Detail panel
        self.detail = QTextEdit()
        self.detail.setReadOnly(True)
        self.detail.setMaximumHeight(180)
        self.detail.setPlaceholderText("选中论文查看详情")
        layout.addWidget(self.detail)

        self.papers: list[dict] = []
        self._feed_thread = None
        self._gap_thread = None

    def _add_interest(self):
        kw = self.interest_input.text().strip()
        if kw and kw not in self.interests:
            self.interests.append(kw)
            tag = QPushButton(f"{kw} ×")
            tag.setStyleSheet(
                "background: #fef3c7; color: #d97706; border: none; "
                "border-radius: 12px; padding: 2px 10px; font-size: 11px;"
            )
            tag.clicked.connect(lambda: self._remove_interest(kw, tag))
            self.interest_tags.addWidget(tag)
            self.interest_tags.addWidget(tag)
        self.interest_input.clear()

    def _remove_interest(self, kw: str, tag: QPushButton):
        self.interests.remove(kw)
        tag.deleteLater()

    def _load_feed(self):
        self.feed_btn.setEnabled(False)
        self.feed_btn.setText("加载中...")
        self._feed_thread = FeedThread(self.interests)
        self._feed_thread.done.connect(self._on_feed)
        self._feed_thread.start()

    def _on_feed(self, papers, errors):
        self.feed_btn.setEnabled(True)
        self.feed_btn.setText("刷新 Feed")
        self.papers = papers
        self.paper_list.clear()
        for p in papers:
            title = p.get("title", "Untitled")[:100]
            authors = p.get("authors", "")[:50]
            item = QListWidgetItem(f"{title}\n{authors}")
            item.setData(1, p)
            self.paper_list.addItem(item)

    def _show_paper_detail(self, idx: int):
        if idx < 0 or idx >= len(self.papers):
            return
        p = self.papers[idx]
        text = f"Title: {p.get('title', '')}\n"
        text += f"Authors: {p.get('authors', '')}\n"
        text += f"Published: {p.get('published', '')}\n"
        text += f"Link: {p.get('link', '')}\n"
        text += f"Venue: {p.get('venue', '')}\n\n"
        text += p.get("summary", "")
        self.detail.setText(text)

    def _find_gaps(self):
        if not self.papers:
            return
        self.gap_btn.setEnabled(False)
        self._gap_thread = GapThread(self.papers)
        self._gap_thread.done.connect(self._on_gaps)
        self._gap_thread.start()

    def _on_gaps(self, gaps):
        self.gap_btn.setEnabled(True)
        self.detail.clear()
        text = "=== 研究方向空白分析 ===\n\n"
        for g in gaps:
            conf = "HIGH" if g["confidence"] == "high" else "MED"
            text += f"[{conf}] {g['direction']}\n  {g['reason']}\n\n"
        self.detail.setText(text)
