from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt


class DashboardPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        title = QLabel("📊 System Overview")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:26px;font-weight:bold;")

        info = QLabel("Live system monitoring dashboard")
        info.setAlignment(Qt.AlignCenter)
        info.setStyleSheet("color:#94A3B8;")

        layout.addWidget(title)
        layout.addWidget(info)
        layout.addStretch()

        self.setLayout(layout)