import sys
import os
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QScrollArea, QMainWindow, QFrame
from PyQt5.QtCore import Qt, QPropertyAnimation, QSize, QTimer
from PyQt5.QtGui import QColor, QPalette, QIcon, QFont,QIntValidator

class Log(QFrame):
    def __init__(self, text):
        super().__init__()
        self.setStyleSheet("""
            border: 2px solid black;
            background-color: #d0d0d0;
        """)
        self.setFixedSize(900, 200)

        # Add a label inside the box
        label = QLabel(text, self)
        label.setAlignment(Qt.AlignCenter)

class ScrollAreaExample(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aktivitas Fisik")
        self.resize(500, 500)

        #Initialize
        self.header = QLabel("Aktivitas Fisik")

        #Begin modifying
        self.header.setAlignment(Qt.AlignHCenter)
        self.header.setFont(QFont("Arial", 30))

        #Begin Layout
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.header)
        for i in range(5):
            self.log = Log(f"Testing, {i}")
            self.layout.addWidget(self.log)
        self.setLayout(self.layout)



if __name__ == "__main__":
    app = QApplication([])
    window = ScrollAreaExample()
    window.show()
    sys.exit(app.exec_())