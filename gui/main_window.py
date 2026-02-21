import sys
import psutil
import pyqtgraph as pg

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QPushButton,
    QGridLayout, QFrame
)
from PySide6.QtCore import Qt, QTimer


# ===============================
# Card Widget
# ===============================

def create_card(title, value):

    card = QFrame()
    card.setObjectName("Card")

    layout = QVBoxLayout()

    title_lbl = QLabel(title)
    title_lbl.setObjectName("CardTitle")

    value_lbl = QLabel(value)
    value_lbl.setObjectName("CardValue")

    layout.addWidget(title_lbl)
    layout.addWidget(value_lbl)

    card.setLayout(layout)

    return card


# ===============================
# Main Window
# ===============================

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Linux Smart Monitor")
        self.setMinimumSize(1200, 700)

        # ================= MAIN =================

        main_widget = QWidget()
        main_layout = QHBoxLayout()

        # ================= SIDEBAR =================

        sidebar_layout = QVBoxLayout()

        title = QLabel("⚡ Smart Monitor")
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("Title")

        btn_dashboard = QPushButton("Dashboard")
        btn_memory = QPushButton("Memory")
        btn_process = QPushButton("Processes")
        btn_settings = QPushButton("Settings")

        sidebar_layout.addWidget(title)
        sidebar_layout.addSpacing(20)
        sidebar_layout.addWidget(btn_dashboard)
        sidebar_layout.addWidget(btn_memory)
        sidebar_layout.addWidget(btn_process)
        sidebar_layout.addWidget(btn_settings)
        sidebar_layout.addStretch()

        sidebar = QWidget()
        sidebar.setLayout(sidebar_layout)
        sidebar.setObjectName("Sidebar")

        # ================= CONTENT =================

        self.content_layout = QVBoxLayout()

        welcome = QLabel("Welcome to Smart Monitor Dashboard")
        welcome.setAlignment(Qt.AlignCenter)
        welcome.setObjectName("Content")

        self.content_layout.addWidget(welcome)
        self.content_layout.addSpacing(15)

        # ================= STATS =================

        self.stats_panel = self.create_stats_panel()
        self.content_layout.addWidget(self.stats_panel)

        self.content_layout.addSpacing(25)

        # ================= GRAPHS =================

        self.init_graphs()

        self.content_layout.addWidget(self.cpu_plot)
        self.content_layout.addWidget(self.ram_plot)

        self.content_layout.addStretch()

        content = QWidget()
        content.setLayout(self.content_layout)

        # ================= ADD =================

        main_layout.addWidget(sidebar, 1)
        main_layout.addWidget(content, 4)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # ================= TIMER =================

        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_all)
        self.timer.start(2000)


    # ===============================
    # Create Stats Panel
    # ===============================

    def create_stats_panel(self):

        grid = QGridLayout()

        cpu = f"{psutil.cpu_percent()}%"
        ram = f"{psutil.virtual_memory().percent}%"
        disk = f"{psutil.disk_usage('/').percent}%"
        net = f"{round(psutil.net_io_counters().bytes_recv / 1024, 2)} KB"

        self.cpu_card = create_card("CPU Usage", cpu)
        self.ram_card = create_card("RAM Usage", ram)
        self.disk_card = create_card("Disk Usage", disk)
        self.net_card = create_card("Network", net)

        grid.addWidget(self.cpu_card, 0, 0)
        grid.addWidget(self.ram_card, 0, 1)
        grid.addWidget(self.disk_card, 0, 2)
        grid.addWidget(self.net_card, 0, 3)

        panel = QWidget()
        panel.setLayout(grid)

        return panel


    # ===============================
    # Init Graphs
    # ===============================

    def init_graphs(self):

        pg.setConfigOptions(antialias=True)

        self.cpu_data = [0] * 50
        self.ram_data = [0] * 50

        # CPU Graph
        self.cpu_plot = pg.PlotWidget(title="CPU Usage (%)")
        self.cpu_plot.setBackground("#020617")
        self.cpu_plot.showGrid(x=True, y=True, alpha=0.3)

        self.cpu_curve = self.cpu_plot.plot(
            self.cpu_data,
            pen=pg.mkPen("#38BDF8", width=2)
        )

        # RAM Graph
        self.ram_plot = pg.PlotWidget(title="RAM Usage (%)")
        self.ram_plot.setBackground("#020617")
        self.ram_plot.showGrid(x=True, y=True, alpha=0.3)

        self.ram_curve = self.ram_plot.plot(
            self.ram_data,
            pen=pg.mkPen("#22C55E", width=2)
        )


    # ===============================
    # Update Stats
    # ===============================

    def update_stats(self):

        cpu = f"{psutil.cpu_percent()}%"
        ram = f"{psutil.virtual_memory().percent}%"
        disk = f"{psutil.disk_usage('/').percent}%"
        net = f"{round(psutil.net_io_counters().bytes_recv / 1024, 2)} KB"

        self.cpu_card.findChild(QLabel, "CardValue").setText(cpu)
        self.ram_card.findChild(QLabel, "CardValue").setText(ram)
        self.disk_card.findChild(QLabel, "CardValue").setText(disk)
        self.net_card.findChild(QLabel, "CardValue").setText(net)


    # ===============================
    # Update Graphs
    # ===============================

    def update_graphs(self):

        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent

        self.cpu_data = self.cpu_data[1:] + [cpu]
        self.ram_data = self.ram_data[1:] + [ram]

        self.cpu_curve.setData(self.cpu_data)
        self.ram_curve.setData(self.ram_data)


    # ===============================
    # Refresh Everything
    # ===============================

    def refresh_all(self):

        self.update_stats()
        self.update_graphs()