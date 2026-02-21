import psutil

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QProgressBar
)
from PySide6.QtCore import Qt, QTimer


class MemoryPage(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        title = QLabel("💾 Memory Monitor")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:26px;font-weight:bold;")

        self.ram_label = QLabel()
        self.swap_label = QLabel()

        self.ram_bar = QProgressBar()
        self.swap_bar = QProgressBar()

        self.ram_bar.setMaximum(100)
        self.swap_bar.setMaximum(100)

        self.ram_bar.setFixedHeight(25)
        self.swap_bar.setFixedHeight(25)

        self.layout.addWidget(title)
        self.layout.addSpacing(20)

        self.layout.addWidget(QLabel("RAM Usage"))
        self.layout.addWidget(self.ram_bar)
        self.layout.addWidget(self.ram_label)

        self.layout.addSpacing(15)

        self.layout.addWidget(QLabel("Swap Usage"))
        self.layout.addWidget(self.swap_bar)
        self.layout.addWidget(self.swap_label)

        self.layout.addStretch()

        self.setLayout(self.layout)

        # Update timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_memory)
        self.timer.start(2000)

        self.update_memory()


    def update_memory(self):

        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()

        self.ram_bar.setValue(int(mem.percent))
        self.swap_bar.setValue(int(swap.percent))

        self.ram_label.setText(
            f"{mem.used//1024**2} MB / {mem.total//1024**2} MB"
        )

        self.swap_label.setText(
            f"{swap.used//1024**2} MB / {swap.total//1024**2} MB"
        )