"""问一问 — chat widget."""

import asyncio

from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTextEdit, QLineEdit, QPushButton, QScrollArea, QFrame,
    QComboBox,
)

from backend.core.llm_router import LLMRouter


class ChatThread(QThread):
    reply = Signal(str)

    def __init__(self, router: LLMRouter, messages: list[dict], classification: str):
        super().__init__()
        self.router = router
        self.messages = messages
        self.classification = classification

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            provider = self.router.select(classification=self.classification)
            result = loop.run_until_complete(
                self.router.chat(provider, self.messages)
            )
            self.reply.emit(result)
        except Exception as e:
            self.reply.emit(f"出错了: {str(e)}")
        finally:
            loop.close()


class ChatWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        header = QFrame()
        header.setFixedHeight(44)
        header.setStyleSheet(
            "background: #faf5ee; border-bottom: 1px solid #f0e8db;"
        )
        hl = QHBoxLayout(header)
        hl.addWidget(QLabel("问一问"))
        hl.addStretch()
        self.classification = QComboBox()
        self.classification.addItems(["审慎", "公开"])
        hl.addWidget(self.classification)
        layout.addWidget(header)

        # Messages
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.msg_widget = QWidget()
        self.msg_layout = QVBoxLayout(self.msg_widget)
        self.msg_layout.addStretch()
        self.scroll.setWidget(self.msg_widget)
        layout.addWidget(self.scroll, 1)

        # Input
        input_frame = QFrame()
        input_frame.setStyleSheet("border-top: 1px solid #f0e8db;")
        il = QHBoxLayout(input_frame)
        self.input = QLineEdit()
        self.input.setPlaceholderText("说点什么...")
        self.input.returnPressed.connect(self._send)
        il.addWidget(self.input)
        send_btn = QPushButton("↑")
        send_btn.setFixedWidth(36)
        send_btn.clicked.connect(self._send)
        il.addWidget(send_btn)
        layout.addWidget(input_frame)

        self.messages: list[dict] = []
        self.router = LLMRouter()
        self._chat_thread = None

    def _send(self):
        text = self.input.text().strip()
        if not text:
            return

        self.input.clear()
        self._add_message("user", text)
        self.messages.append({"role": "user", "content": text})

        cls = "cautious" if self.classification.currentIndex() == 0 else "public"
        self._chat_thread = ChatThread(self.router, list(self.messages), cls)
        self._chat_thread.reply.connect(self._on_reply)
        self._chat_thread.start()

    def _on_reply(self, text: str):
        self._add_message("assistant", text)
        self.messages.append({"role": "assistant", "content": text})

    def _add_message(self, role: str, content: str):
        bubble = QFrame()
        is_user = role == "user"
        bubble.setStyleSheet(
            "background: #fef3c7; border-radius: 12px; padding: 8px 12px;"
            if is_user else
            "background: #fffbf7; border: 1px solid #f0e8db; border-radius: 12px; padding: 8px 12px;"
        )
        bl = QHBoxLayout(bubble)
        if is_user:
            bl.addStretch()
        lbl = QLabel(content)
        lbl.setWordWrap(True)
        lbl.setMaximumWidth(220)
        lbl.setStyleSheet("font-size: 12px;")
        bl.addWidget(lbl)
        if not is_user:
            bl.addStretch()

        # Insert before the stretch
        self.msg_layout.insertWidget(self.msg_layout.count() - 1, bubble)
