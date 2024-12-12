import sys
import os
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QScrollArea, 
QMainWindow, QFrame, QPushButton, QSpacerItem, QMessageBox)
from PyQt5.QtCore import Qt, QPropertyAnimation, QSize, QTimer
from PyQt5.QtGui import QColor, QPalette, QIcon, QFont,QIntValidator

class Log(QFrame):
    def __init__(self, parent_layout):
        super().__init__()
        self.parent_layout = parent_layout

        self.setStyleSheet("""
            border: 2px solid black;
            background-color: #d0d0d0;
        """)
        self.setFixedSize(1000, 300)

        # Add a label inside the box
        self.box_area = QHBoxLayout(self)
        self.text_area = QVBoxLayout()
        self.text1 = QLabel(f"Date : ")
        self.text2 = QLabel("Calories burned : ")
        self.text3 = QLabel("Steps : ")

        self.text1.setStyleSheet("border:none; font-family: Arial; font-size:30px;")
        self.text2.setStyleSheet("border:none; font-family: Arial; font-size:30px;")
        self.text3.setStyleSheet("border:none; font-family: Arial; font-size:30px;")

        self.remove_button = QPushButton("X")
        self.remove_button.setFixedSize(50, 30)  # Set button size
        self.remove_button.setStyleSheet("""
            QPushButton {
            background-color: #de0735; color: white; border: none; border-radius: 5px;
            }
            QPushButton:hover{
                background-color: #a6021d; 
            }
        """)
        self.remove_button.clicked.connect(self.confirm_removal)

        self.row0 = QHBoxLayout()
        self.row0.addStretch()
        self.row0.addWidget(self.remove_button)
        self.row0.setAlignment(self.remove_button, Qt.AlignTop)

        self.text_area.addWidget(self.text1)
        self.text_area.addWidget(self.text2)
        self.text_area.addWidget(self.text3)
        self.box_area.addLayout(self.text_area)
        self.box_area.addLayout(self.row0)
    
    def confirm_removal(self):
        dialog = QMessageBox(self)
        dialog.setWindowTitle("Konfirmasi Hapus")
        dialog.setText("Apakah Anda yakin ingin menghapus log ini")
        #Iconnya jelek anjir ada border itemnnya
        #dialog.setIcon(QMessageBox.Warning)
        dialog.setMinimumSize(500, 500)
        
        yes_button = dialog.addButton(QMessageBox.Yes)
        no_button = dialog.addButton(QMessageBox.No)
        dialog.setStyleSheet("""
            QMessageBox {
                background-color: #d0d0d0; /* Ensure no background for icons */
                color: black;
                border: none;
                padding: 5px 15px;
                font-size: 14px;
            }
            QMessageBox QLabel {
                border: none;
                font-size: 30px;
                color: #333;
            }
                             
            QMessageBox Icon {
                border: none;
            }
        """)

        yes_button.setStyleSheet("""
            QPushButton {
                min-width: 80px;
                min-height: 30px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 15px;
                font-size: 20px;
            }
                                 
            QPushButton:hover{
                background-color: #106309;
            }
        """
        )

        no_button.setStyleSheet("""
            QPushButton {
                min-width: 80px;
                min-height: 30px;
                background-color: #de0735;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 15px;
                font-size: 20px;
            }
            
            QPushButton:hover{
                background-color: #a6021d;
            }
        """
        )
        # Show the dialog and get the response
        response = dialog.exec_()
        if response == QMessageBox.Yes:
            self.remove_box()
        else:
            pass

    def remove_box(self):
        if self is not None:
            self.parent_layout.removeWidget(self)
            self.deleteLater()  # Deletes the widget



class ActivityUI(QWidget):
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
            self.log = Log(self.box_layout)
            self.box_layout.addWidget(self.log)
        

if __name__ == "__main__":
    app = QApplication([])
    window = ActivityUI()
    window.show()
    sys.exit(app.exec_())