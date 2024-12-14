import sys
import os
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QScrollArea, 
QMainWindow, QFrame, QPushButton, QSpacerItem, QMessageBox, QComboBox, QLineEdit, QStackedLayout, QDateTimeEdit, QSizePolicy)
from PyQt5.QtCore import Qt, QPropertyAnimation, QSize, QTimer, QDate, QDateTime
from PyQt5.QtGui import QColor, QPalette, QIcon, QFont,QIntValidator

from backend.controllers.AktivitasFisikController import *

class Log(QFrame):
    def __init__(self, parent_layout, db_fileName, data_log):
        self.db_fileName = db_fileName
        self._data_log = data_log
        super().__init__()
        self.parent_layout = parent_layout
        self.setStyleSheet("""
            border: none;
            background-color: #ffffff;
        """)
        self.setFixedSize(1000, 300)
        self.date = data_log['date']
        self.time = data_log['jam']
        self.activity = data_log['nama_aktivitas']
        self.achievement = data_log['capaian']
        self.calorie = data_log['kalori']
        # Add a label inside the box
        self.box_area = QHBoxLayout(self)
        self.text_area = QVBoxLayout()
        self.text1 = QLabel(f"Date : {self.date}")
        self.text2 = QLabel(f"Time : {self.time}")
        self.text3 = QLabel(f"Activity: {self.activity}")
        self.text4 = QLabel(f"Achieved : {self.achievement}")
        self.text5 = QLabel(f"Calories burned : {self.calorie}")

        self.text1.setStyleSheet("border:none; font-family: Arial; font-size:30px;")
        self.text2.setStyleSheet("border:none; font-family: Arial; font-size:30px;")
        self.text3.setStyleSheet("border:none; font-family: Arial; font-size:30px;")
        self.text4.setStyleSheet("border:none; font-family: Arial; font-size:30px;")
        self.text5.setStyleSheet("border:none; font-family: Arial; font-size:30px;")

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
        self.text_area.addWidget(self.text4)
        self.text_area.addWidget(self.text5)
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
            self.remove_log()
        else:
            pass

    def remove_log(self):
        if self is not None:
            print(self._data_log)
            AktivitasFisikController(self.db_fileName).deleteAktivitas(self._data_log)
            self.parent_layout.removeWidget(self)
            self.deleteLater()  # Deletes the widget

class ActivityForm(QWidget):
    def __init__(self, switch_to_ui, db_fileName):
        super().__init__()
        self.switch_to_ui = switch_to_ui
        self.db_fileName = db_fileName
        self.layout = QVBoxLayout(self)
        subheader = QLabel("Form Log Aktivitas Fisik Baru")
        subheader.setStyleSheet("""
        font-size:50px;
        font-family:Arial;
        """)
        #Lame fix, but works
        policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        subheader.setSizePolicy(policy)
        self.form_box = QFrame()
        self.form_box.setStyleSheet("""
        QFrame {
            border: black solid 2px;
            background-color: #ffffff;
            padding : 5px;
        }
        """)
        self.form_box.setFixedSize(2000, 600)
        self.form_layout = QVBoxLayout(self.form_box)

        #JANGAN LUPA UBAH TANGGAL DARI GARING KE YY-MM-DD
        self.date_form = QDateTimeEdit()
        self.date_form.setDateTime(QDateTime.currentDateTime())
        self.activity_form = QComboBox()
        input_list = ListAktivitasController(self.db_fileName).getListAktivitasValid()
        for i in input_list:
            self.activity_form.addItem(i)
        self.achievement_form = QLineEdit()
        self.achievement_form.setFixedWidth(200)
        ach_validator = QIntValidator(0, 1000)
        self.achievement_form.setValidator(ach_validator)
        self.calorie_form = QLineEdit()
        self.calorie_form.setFixedWidth(200)
        cal_validator = QIntValidator(0, 3000)
        self.calorie_form.setValidator(cal_validator)

        self.date_form.setStyleSheet("""
            QDateEdit {
                border: 2px solid #0078d7; /* Blue border */
                border-radius: 5px;       /* Rounded corners */
                padding: 2px;
            }
        """)

        self.activity_form.setStyleSheet("""
            QDateEdit {
                border: 2px solid #0078d7; /* Blue border */
                border-radius: 5px;       /* Rounded corners */
                padding: 2px;
            }
        """)

        self.achievement_form.setStyleSheet("""
            QDateEdit {
                border: 2px solid #0078d7; /* Blue border */
                border-radius: 5px;       /* Rounded corners */
                padding: 2px;
            }
        """)

        self.calorie_form.setStyleSheet("""
            QDateEdit {
                border: 2px solid #0078d7; /* Blue border */
                border-radius: 5px;       /* Rounded corners */
                padding: 2px;
            }
        """)

        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        row3 = QHBoxLayout()
        row4 = QHBoxLayout()

        text1 = QLabel("Tanggal & Waktu: ")
        text2 = QLabel("Aktivitas : ")
        text3 = QLabel("Capaian : ")
        text4 = QLabel("Kalori : ")

        text1.setStyleSheet("border:none; font-family: Arial; font-size:40px;")
        text2.setStyleSheet("border:none; font-family: Arial; font-size:40px;")
        text3.setStyleSheet("border:none; font-family: Arial; font-size:40px;")
        text4.setStyleSheet("border:none; font-family: Arial; font-size:40px;")

        row1.addWidget(text1)
        row1.addWidget(self.date_form)
        row2.addWidget(text2)
        row2.addWidget(self.activity_form)
        row3.addWidget(text3)
        row3.addWidget(self.achievement_form)
        row4.addWidget(text4)
        row4.addWidget(self.calorie_form)

        self.form_layout.addLayout(row1)
        self.form_layout.addLayout(row2)
        self.form_layout.addLayout(row3)
        self.form_layout.addLayout(row4)

        button_row = QHBoxLayout()
        add_button = QPushButton("Add")
        cancel_button = QPushButton("Cancel")
        add_button.setStyleSheet("""
            QPushButton {
                min-width: 160px;
                min-height: 60px;
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

        cancel_button.setStyleSheet("""
            QPushButton {
                min-width: 160px;
                min-height: 60px;
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
        add_button.clicked.connect(self.confirm_adding)
        cancel_button.clicked.connect(self.switch_to_ui)
        self.layout.addWidget(subheader)
        self.layout.addWidget(self.form_box, alignment= Qt.AlignHCenter | Qt.AlignTop)
        subheader.setAlignment(Qt.AlignCenter)
        #self.form_box.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        button_row.addStretch()
        button_row.addWidget(add_button)
        button_row.addWidget(cancel_button)
        button_row.setAlignment(Qt.AlignTop)
        button_row.addStretch()
        self.layout.addLayout(button_row)
        self.setLayout(self.layout)
    
    def confirm_adding(self):
        dialog = QMessageBox(self)
        dialog.setWindowTitle("Konfirmasi")
        dialog.setText("Apakah Anda yakin ingin menambah log ini?")
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
            data_log = {}
            data_log["date"] = self.date_form.date()
            data_log["jam"] = self.date_form.time()
            data_log["nama_aktivitas"] = self.activity_form.currentText()
            data_log["capaian"] = self.achievement_form.text()
            data_log["kalori"] = self.calorie_form.text()
            AktivitasFisikController(self.db_fileName).addAktivitas(data_log)
            #self.parent().show_logs()
            self.switch_to_ui()
        else:
            pass
            

class ActivityUI(QWidget):
    def __init__(self, db_fileName):
        super().__init__()
        self.setWindowTitle("Aktivitas Fisik")
        self.resize(500, 500)
        self.setStyleSheet("background-color: #f5f5f5;")
        self.db_fileName = db_fileName

        #Initialize
        self.master_layout = QVBoxLayout(self)
        self.header = QLabel("Aktivitas Fisik")
        self.log_menu = QWidget()
        self.log_menu_layout = QVBoxLayout(self.log_menu)
        button_row = QHBoxLayout()
        self.add_button = QPushButton("Tambah Log Baru")
        self.add_button.setStyleSheet("""
        QPushButton {
                background-color: #3c4a71;       /* Blue background */
                color: white;                /* White text */
                border: none;                /* No border */
                border-radius: 15px;         /* Rounded corners */
                font-size: 25px;             /* Font size */
                padding: 10px;               /* Padding inside the button */
                font-family: Arial;
                height:40px;
                width: 250px;
            }
            QPushButton:hover {
                background-color: #222b42;  /* Darker blue on hover */
            }
        """)
        self.add_button.clicked.connect(self.toggle_form)
        self.log_area = QScrollArea()
        self.log_area.setWidgetResizable(True)
        self.box_container = QWidget()
        self.log_area.setWidget(self.box_container)
        self.box_layout = QVBoxLayout(self.box_container)
        self.box_layout.setAlignment(Qt.AlignTop)  # Align boxes at the top

        self.stacked_layout = QStackedLayout()
        self.form = ActivityForm(self.toggle_form, self.db_fileName)
        self.stacked_layout.addWidget(self.log_menu)
        self.stacked_layout.addWidget(self.form)

        #Begin modifying
        self.header.setAlignment(Qt.AlignHCenter)
        self.header.setFont(QFont("Arial", 30))
        #self.row1.addStretch()
        button_row.addStretch()
        button_row.addWidget(self.add_button)
        self.log_menu_layout.addLayout(button_row)

        #Begin Layout
        self.master_layout.addWidget(self.header)
        self.log_menu_layout.addWidget(self.log_area)
        self.master_layout.addLayout(self.stacked_layout)
        self.displayed_log = ListAktivitasController(self.db_fileName).getListAktivitas()
        for data in self.displayed_log:
            #Sementara kyk gini
            self.log = Log(self.log_menu_layout, self.db_fileName, data_log=data)
            self.box_layout.addWidget(self.log)
        
    # def show_form(self): 
    #     self.stacked_layout.setCurrentWidget(self.form)

    # def show_log_area(self): 
    #     self.stacked_layout.setCurrentWidget(self.log_area)

    def toggle_form(self):
        """Toggle between pages."""
        current_index = self.stacked_layout.currentIndex()
        next_index = (current_index + 1) % self.stacked_layout.count()
        self.stacked_layout.setCurrentIndex(next_index)

if __name__ == "__main__":
    app = QApplication([])
    window = ActivityUI()
    window.showMaximized()
    window.show()
    sys.exit(app.exec_())