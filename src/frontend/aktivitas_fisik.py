import sys
import os
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QScrollArea, QMainWindow, QFrame, QPushButton, QSpacerItem
from PyQt5.QtCore import Qt, QPropertyAnimation, QSize, QTimer
from PyQt5.QtGui import QColor, QPalette, QIcon, QFont,QIntValidator

class Log(QFrame):
    def __init__(self, text):
        super().__init__()
        self.setStyleSheet("""
            border: 2px solid black;
            background-color: #d0d0d0;
        """)
        self.setFixedSize(1000, 300)

        # Add a label inside the box
        self.box_area = QVBoxLayout(self)
        self.text1 = QLabel("Date : ")
        self.text2 = QLabel("Calories burned : ")
        self.text3 = QLabel("Steps : ")

        self.text1.setStyleSheet("border:none; font-family: Arial; font-size:30px;")
        self.text2.setStyleSheet("border:none; font-family: Arial; font-size:30px; padding-top:1px;")
        self.text3.setStyleSheet("border:none; font-family: Arial; font-size:30px; padding-top:2px;")


        self.remove_button = QPushButton("X")
        self.remove_button.setFixedSize(50, 30)  # Set button size
        self.remove_button.setStyleSheet("background-color: #de0735; color: white; border: none; border-radius: 5px;")  # Style the button
        self.row0 = QHBoxLayout()
        self.row0.addStretch()
        self.row0.addWidget(self.remove_button)

        self.row1 = QHBoxLayout()
        self.row1.addWidget(self.text1)

        self.row2 = QHBoxLayout()
        self.row2.addWidget(self.text2)

        self.row3 = QHBoxLayout()
        self.row3.addWidget(self.text3)

        self.box_area.addLayout(self.row0)
        self.box_area.addLayout(self.row1)
        self.box_area.addLayout(self.row2)
        self.box_area.addLayout(self.row3)

class ScrollAreaExample(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aktivitas Fisik")
        self.resize(500, 500)

        #Initialize
        self.header = QLabel("Aktivitas Fisik")
        self.layout = QVBoxLayout(self)
        self.log_area = QScrollArea()
        self.log_area.setWidgetResizable(True)
        self.box_container = QWidget()
        self.box_layout = QVBoxLayout(self.box_container)
        self.box_layout.setAlignment(Qt.AlignTop)  # Align boxes at the top
        self.log_area.setWidget(self.box_container)

        #Begin modifying
        self.header.setAlignment(Qt.AlignHCenter)
        self.header.setFont(QFont("Arial", 30))

        #Begin Layout
        self.layout.addWidget(self.header)
        self.layout.addWidget(self.log_area)
        for i in range(10):
            self.log = Log(f"Testing, {i}")
            self.box_layout.addWidget(self.log)
        

        self.setLayout(self.layout)

if __name__ == "__main__":
    app = QApplication([])
    window = ScrollAreaExample()
    window.show()
    sys.exit(app.exec_())