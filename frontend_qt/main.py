"""研墨 — Native Qt Desktop Application."""

import sys
from pathlib import Path

# Ensure project root is on path
sys.path.insert(0, str(Path(__file__).parent.parent))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from frontend_qt.main_window import MainWindow


def main():
    # High DPI support
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    app = QApplication(sys.argv)
    app.setApplicationName("研墨")
    app.setOrganizationName("YanMo")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
