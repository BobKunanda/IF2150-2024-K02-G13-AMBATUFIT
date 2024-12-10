import sys
import os
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QScrollArea, QMainWindow, QFrame
from PyQt5.QtCore import Qt, QPropertyAnimation, QSize, QTimer
from PyQt5.QtGui import QColor, QPalette, QIcon, QFont,QIntValidator


class ScrollAreaExample(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aktivitas Fisik")
        self.resize(500, 500)

        self.header = QLabel("Aktivitas Fisik")
        self.header.setAlignment(Qt.AlignHCenter)
        self.header.setFont(QFont("Arial", 30))

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.header)

        self.setLayout(self.layout)



if __name__ == "__main__":
    app = QApplication([])
    window = ScrollAreaExample()
    window.show()
    sys.exit(app.exec_())