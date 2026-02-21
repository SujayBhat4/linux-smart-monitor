from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QCheckBox, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt


class SettingsPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        title = QLabel("⚙ Application Settings")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:26px;font-weight:bold;")

        self.auto_start = QCheckBox("Start app on system boot")
        self.notifications = QCheckBox("Enable notifications")
        self.dark_mode = QCheckBox("Force dark theme")

        save_btn = QPushButton("Save Settings")

        save_btn.clicked.connect(self.save_settings)

        layout.addWidget(title)
        layout.addSpacing(20)

        layout.addWidget(self.auto_start)
        layout.addWidget(self.notifications)
        layout.addWidget(self.dark_mode)

        layout.addSpacing(25)
        layout.addWidget(save_btn)

        layout.addStretch()

        self.setLayout(layout)


    def save_settings(self):

        QMessageBox.information(
            self,
            "Settings",
            "Settings saved successfully!"
        )