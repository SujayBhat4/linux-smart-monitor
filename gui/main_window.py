import sys
import psutil
import pyqtgraph as pg

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QGridLayout,
    QFrame,
    QStackedWidget
)

from PySide6.QtCore import Qt, QTimer


# Import Pages
from gui.pages.dashboard_page import DashboardPage
from gui.pages.memory_page import MemoryPage
from gui.pages.settings_page import SettingsPage


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
        self.setMinimumSize(1200, 780)

        # ================= MAIN =================

        main_widget = QWidget()
        main_layout = QHBoxLayout()

        # ================= SIDEBAR =================

        sidebar_layout = QVBoxLayout()

        title = QLabel("⚡ Smart Monitor")
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("Title")

        self.btn_dashboard = QPushButton("Dashboard")
        self.btn_memory = QPushButton("Memory")
        self.btn_settings = QPushButton("Settings")

        sidebar_layout.addWidget(title)
        sidebar_layout.addSpacing(20)

        sidebar_layout.addWidget(self.btn_dashboard)
        sidebar_layout.addWidget(self.btn_memory)
        sidebar_layout.addWidget(self.btn_settings)

        sidebar_layout.addStretch()

        sidebar = QWidget()
        sidebar.setLayout(sidebar_layout)
        sidebar.setObjectName("Sidebar")

        # ================= PAGES =================

        self.pages = QStackedWidget()

        # Dashboard Page (YOUR MAIN UI)
        self.dashboard_page = QWidget()
        self.dashboard_layout = QVBoxLayout()

        # Welcome
        welcome = QLabel("Welcome to Smart Monitor Dashboard")
        welcome.setAlignment(Qt.AlignCenter)
        welcome.setObjectName("Content")

        self.dashboard_layout.addWidget(welcome)
        self.dashboard_layout.addSpacing(10)

        # Stats
        self.stats_panel = self.create_stats_panel()
        self.dashboard_layout.addWidget(self.stats_panel)

        self.dashboard_layout.addSpacing(15)

        # Graphs
        self.init_graphs()

        self.dashboard_layout.addWidget(self.cpu_plot)
        self.dashboard_layout.addWidget(self.ram_plot)

        self.dashboard_layout.addSpacing(20)

        # Health Button
        self.health_btn = QPushButton("System Health: -- / 100")
        self.health_btn.setFixedHeight(50)
        self.health_btn.setEnabled(False)

        self.health_btn.setStyleSheet("""
            QPushButton{
                border-radius:25px;
                font-size:20px;
                font-weight:bold;
                background:#020617;
                color:white;
                border:2px solid #334155;
            }
        """)

        self.dashboard_layout.addWidget(
            self.health_btn,
            alignment=Qt.AlignCenter
        )

        self.dashboard_layout.addStretch()

        self.dashboard_page.setLayout(self.dashboard_layout)

        # Other Pages
        self.memory_page = MemoryPage()
        self.settings_page = SettingsPage()

        # Add to stack
        self.pages.addWidget(self.dashboard_page)   # Index 0
        self.pages.addWidget(self.memory_page)      # Index 1
        self.pages.addWidget(self.settings_page)    # Index 2

        # ================= MAIN LAYOUT =================

        main_layout.addWidget(sidebar, 1)
        main_layout.addWidget(self.pages, 4)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # ================= NAVIGATION =================

        self.btn_dashboard.clicked.connect(
            lambda: self.pages.setCurrentIndex(0)
        )

        self.btn_memory.clicked.connect(
            lambda: self.pages.setCurrentIndex(1)
        )

        self.btn_settings.clicked.connect(
            lambda: self.pages.setCurrentIndex(2)
        )

        # ================= TIMER =================

        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_all)
        self.timer.start(2000)


    # ===============================
    # Stats Panel
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
    # Graphs
    # ===============================

    def init_graphs(self):

        pg.setConfigOptions(antialias=True)

        self.cpu_data = [0] * 50
        self.ram_data = [0] * 50

        self.cpu_plot = pg.PlotWidget(title="CPU Usage (%)")
        self.cpu_plot.setBackground("#020617")
        self.cpu_plot.showGrid(x=True, y=True, alpha=0.3)

        self.cpu_curve = self.cpu_plot.plot(
            self.cpu_data,
            pen=pg.mkPen("#38BDF8", width=2)
        )

        self.ram_plot = pg.PlotWidget(title="RAM Usage (%)")
        self.ram_plot.setBackground("#020617")
        self.ram_plot.showGrid(x=True, y=True, alpha=0.3)

        self.ram_curve = self.ram_plot.plot(
            self.ram_data,
            pen=pg.mkPen("#22C55E", width=2)
        )


    # ===============================
    # Stats Update
    # ===============================

    def update_stats(self):

        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        net = round(psutil.net_io_counters().bytes_recv / 1024, 2)

        self.cpu_card.findChild(QLabel, "CardValue").setText(f"{cpu}%")
        self.ram_card.findChild(QLabel, "CardValue").setText(f"{ram}%")
        self.disk_card.findChild(QLabel, "CardValue").setText(f"{disk}%")
        self.net_card.findChild(QLabel, "CardValue").setText(f"{net} KB")

        self.update_health(cpu, ram, disk)


    # ===============================
    # Graph Update
    # ===============================

    def update_graphs(self):

        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent

        self.cpu_data = self.cpu_data[1:] + [cpu]
        self.ram_data = self.ram_data[1:] + [ram]

        self.cpu_curve.setData(self.cpu_data)
        self.ram_curve.setData(self.ram_data)


    # ===============================
    # Health Logic
    # ===============================

    def update_health(self, cpu, ram, disk):

        load = (cpu * 0.4) + (ram * 0.4) + (disk * 0.2)

        score = int(100 - load)
        score = max(0, min(score, 100))

        if score >= 70:
            color = "#22C55E"
            glow = "#16A34A"

        elif score >= 50:
            color = "#F59E0B"
            glow = "#D97706"

        else:
            color = "#EF4444"
            glow = "#DC2626"

        self.health_btn.setText(f"System Health: {score} / 100")

        self.health_btn.setStyleSheet(f"""
            QPushButton{{
                border-radius:25px;
                font-size:20px;
                font-weight:bold;
                background:#020617;
                color:{color};
                border:2px solid {color};
                padding:10px 25px;
            }}

            QPushButton:hover{{
                box-shadow:0 0 15px {glow};
            }}
        """)


    # ===============================
    # Refresh
    # ===============================

    def refresh_all(self):

        self.update_stats()
        self.update_graphs()