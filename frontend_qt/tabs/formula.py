"""验公式 — Qt tab."""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTextEdit, QPushButton, QFrame, QSplitter,
)

from backend.plugins.formula.verify import verify_formula, sympy_verify


class FormulaTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)

        notice = QLabel("纯本地计算 (SymPy)，不走 LLM，数据不离开本机")
        notice.setStyleSheet("font-size: 12px; color: #99968e; margin-bottom: 8px;")
        layout.addWidget(notice)

        splitter = QSplitter()
        left = QWidget()
        ll = QVBoxLayout(left)
        ll.setContentsMargins(0, 0, 8, 0)
        ll.addWidget(QLabel("LaTeX 源码"))

        self.input = QTextEdit()
        self.input.setPlaceholderText(
            "粘贴 LaTeX 公式...\n如: \\frac{-b + \\sqrt{b^2 - 4ac}}{2a}"
        )
        self.input.setStyleSheet("font-family: 'JetBrains Mono', monospace;")
        ll.addWidget(self.input)
        splitter.addWidget(left)

        right = QWidget()
        rl = QVBoxLayout(right)
        rl.setContentsMargins(8, 0, 0, 0)
        rl.addWidget(QLabel("渲染预览"))

        self.preview = QLabel("...")
        self.preview.setAlignment(0x0084)  # AlignCenter
        self.preview.setStyleSheet(
            "background: #fffbf7; border: 1px solid #e8e0d5; border-radius: 8px; "
            "font-size: 20px; padding: 20px;"
        )
        rl.addWidget(self.preview)
        splitter.addWidget(right)
        layout.addWidget(splitter, 1)

        self.input.textChanged.connect(
            lambda: self.preview.setText(self.input.toPlainText() or "...")
        )

        self.run_btn = QPushButton("交叉验证")
        self.run_btn.clicked.connect(self._verify)
        layout.addWidget(self.run_btn)

        self.result_area = QFrame()
        self.result_layout = QVBoxLayout(self.result_area)
        layout.addWidget(self.result_area)

    def _verify(self):
        expr = self.input.toPlainText().strip()
        if not expr:
            return

        basic = verify_formula(expr)
        sympy_r = sympy_verify(expr)
        ok = basic.is_valid and sympy_r.is_valid

        # Clear
        while self.result_layout.count():
            item = self.result_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Status
        status = QLabel("双通道验证通过" if ok else "验证发现问题")
        status.setStyleSheet(
            f"background: {'#ecfccb' if ok else '#fef2f2'}; "
            f"border: 1px solid {'#65a30d' if ok else '#dc2626'}; "
            f"border-radius: 8px; padding: 10px 16px; "
            f"font-weight: 600; color: {'#65a30d' if ok else '#dc2626'};"
        )
        self.result_layout.addWidget(status)

        if basic.errors:
            self.result_layout.addWidget(QLabel(f"基本: {'; '.join(basic.errors)}"))
        if basic.warnings:
            self.result_layout.addWidget(QLabel(f"警告: {'; '.join(basic.warnings)}"))
        if sympy_r.suggestions:
            self.result_layout.addWidget(QLabel(f"SymPy: {'; '.join(sympy_r.suggestions)}"))
        if sympy_r.errors:
            self.result_layout.addWidget(QLabel(f"SymPy错误: {'; '.join(sympy_r.errors)}"))
