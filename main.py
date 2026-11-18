import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PySide6.QtGui import QIcon, QPixmap
from database import Database

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()          

        self.setWindowTitle("Мир киберспорта — Каталог")
        self.resize(800, 600)
        self.setWindowIcon(QIcon("resources/icon.ico"))

        self.setStyleSheet("""
            QMainWindow {
                background-color: #FFFFFF;
                font-family: Calibri;
            }
            QLabel {
                color: #000000;
            }
        """)

    def closeEvent(self, event):
        self.db.close_all()
        event.accept()

        central = QWidget()
        layout = QVBoxLayout()

        title = QLabel("Мир киберспорта — Каталог")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        logo = QLabel()
        pixmap = QPixmap("resources/logo.png")
        logo.setPixmap(pixmap)
        logo.setScaledContents(False)
        layout.addWidget(logo)

        central.setLayout(layout)
        self.setCentralWidget(central)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())