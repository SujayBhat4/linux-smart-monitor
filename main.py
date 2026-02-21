import sys
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow


def load_styles(app):
    with open("styles/theme.qss", "r") as f:
        app.setStyleSheet(f.read())


def main():
    app = QApplication(sys.argv)

    load_styles(app)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()