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

        #Initialize
        self.header = QLabel("Aktivitas Fisik")
        #self.log = QScrollArea()
        self.box = QFrame()
        self.text1 = QLabel("Testing", self.box)

        #Begin modifying
        self.header.setAlignment(Qt.AlignHCenter)
        self.header.setFont(QFont("Arial", 30))

        self.box.setFrameShape(QFrame.Box)
        self.box.setLineWidth(2)
        self.box.setStyleSheet("background-color: #f0f0f0;")
        self.box.setFixedSize(900, 200)

        self.text1.setFont(QFont("Arial", 20))
        self.text1.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        #Begin Layout
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.header)
        self.layout.addWidget(self.box)

        self.setLayout(self.layout)



if __name__ == "__main__":
    app = QApplication([])
    window = ScrollAreaExample()
    window.show()
    sys.exit(app.exec_())