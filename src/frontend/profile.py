import sys
import os
from PyQt5.QtWidgets import (QMessageBox,QGraphicsDropShadowEffect, QTextEdit, QVBoxLayout,QSpacerItem, 
                             QSizePolicy, QHBoxLayout, QWidget, QPushButton, QLabel, 
                             QStackedLayout, QLineEdit,QComboBox)
from PyQt5.QtCore import Qt, QPropertyAnimation, QSize, QTimer
from PyQt5.QtGui import QColor, QPalette, QIcon, QFont,QIntValidator
from backend.controllers.PersonalDataController import ProfileController

class Profile(QWidget):
    def __init__(self, db_filename, sidebar = None, home = None):
        super().__init__()
        self.sidebar = sidebar
        self.home = home
        self.controller = ProfileController(db_filename)  
        self.initUI()

    def initUI(self):
        self.profile_data = self.controller.get_profile_data()  
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(20)

        # ---------- Header ----------------
        self.header = QWidget()
        self.header.setMaximumHeight(200)
        self.header.setStyleSheet("""
        QWidget{
            background-color: #4C6A92;
        }
        """)
        headerLayout = QHBoxLayout()
        headerLayout.setContentsMargins(10, 0, 0, 0)
        headerLayout.setSpacing(20)

        self.imageButton = QPushButton()
        imageIcon = QIcon(os.path.abspath("src/assets/icons/profile.png"))
        self.imageButton.setIcon(imageIcon)
        self.imageButton.setIconSize(QSize(90, 90))
        self.imageButton.setFixedSize(90, 90)
        self.imageButton.setStyleSheet(""" 
        QPushButton {
            border-radius: 45px;
            background-color: #ffffff;
            color: white;
            border: 2px solid #2980b9;
        }
        QPushButton:hover {
            background-color: #d3d3d3;
        }
        """)

        self.editButton = QPushButton("Edit Profile")
        self.editButton.adjustSize()
        self.editButton.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 5px;
                border: 2px solid #000000;
                padding: 10px 10px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5dade2;
            }
            QPushButton:pressed {
                background-color: #2980b9;
            }
        """)

        self.editButton.clicked.connect(self.toggleEditMode)

        headerLayout.addWidget(self.imageButton, alignment=Qt.AlignLeft)
        headerLayout.addWidget(self.editButton, alignment=Qt.AlignLeft)
        spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        headerLayout.addItem(spacer)

        self.header.setLayout(headerLayout)
        self.header.setMinimumHeight(150)
        mainLayout.addWidget(self.header)

        # ------------ Footer -------------------------------
        self.footer = QWidget()
        self.footerLayout = QStackedLayout()
        self.footerLayout.setContentsMargins(0, 0, 0, 0)
        self.footerLayout.setSpacing(0)

        self.profileContainer = QWidget()
        self.profileLayout = QVBoxLayout()
        self.profileLayout.setContentsMargins(5, 10, 10, 10)
        self.profileLayout.setSpacing(20)

        self.labels = [("nama","Name"), ("usia","Age"), ("tinggi","Height"), ("berat","Weight"), ("tujuan","Fitness Goal")]
        self.inputFields = {}

        for i, label in enumerate(self.labels):
            container = self.createForm(label[1], self.profile_data[label[0]])  # Gunakan data dari controller
            self.profileLayout.addWidget(container, alignment=Qt.AlignLeft)

        spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.profileLayout.addItem(spacer)
        self.profileContainer.setLayout(self.profileLayout)
        self.footerLayout.addWidget(self.profileContainer)

        self.editContainer = QWidget()
        self.editLayout = QVBoxLayout()
        self.editLayout.setContentsMargins(5, 10, 10, 10)
        self.editLayout.setSpacing(10)

        for i, label in enumerate(self.labels):
            container = self.createEditField(label[1], self.profile_data[label[0]])  # Gunakan data dari controller
            self.editLayout.addWidget(container, alignment=Qt.AlignLeft)

        self.confirmButton = QPushButton("Confirm Changes")
        self.confirmButton.clicked.connect(self.confirmChanges)
        self.confirmButton.setStyleSheet("""
        QPushButton {
            background-color: #27ae60;
            color: white;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 14px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #2ecc71;
        }
        """)

        self.discardButton = QPushButton("Discard Changes")
        self.discardButton.setStyleSheet("""
        QPushButton {
            background-color: #c0392b;
            color: white;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 14px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #e74c3c;
        }
        """)
        self.discardButton.clicked.connect(self.discardChanges)

        self.editLayout.addWidget(self.confirmButton)
        self.editLayout.addWidget(self.discardButton)
        self.editContainer.setLayout(self.editLayout)
        self.footerLayout.addWidget(self.editContainer)

        self.footer.setLayout(self.footerLayout)
        mainLayout.addWidget(self.footer)

        self.setLayout(mainLayout)
        self.isEditing = False

    def toggleEditMode(self):
        self.isEditing = not self.isEditing
        self.footerLayout.setCurrentIndex(int(self.isEditing))
        self.editButton.setVisible(not self.isEditing)

    def createForm(self, label, content):
        formContainer = QWidget()
        textlabel = QLabel()
        layoutForm = QVBoxLayout()
        layoutForm.setContentsMargins(20, 0, 0, 0)
        layoutForm.setSpacing(2)

        content = str(content) if isinstance(content,int) else content
        content = str(content) if isinstance(content,float) else content
        if content == None:
            content = ""

        if label == "Weight":
            textlabel.setText(label.ljust(12) + ":   " + content+" Kg")
        elif label == "Height":
            textlabel.setText(label.ljust(12) + ":   " + content +" Cm")
        else:
            textlabel.setText(label.ljust(12) + ":   " + content)

        layoutForm.addWidget(textlabel)
        textlabel.setStyleSheet("""
        QLabel {
            font-size: 14px;
            font-weight: bold;
            color: #2c3e50;
        }
        """)


        formContainer.setLayout(layoutForm)

        return formContainer

    def createEditField(self, label, content):
        formContainer = QWidget()
        layoutForm = QHBoxLayout()
        layoutForm.setContentsMargins(20, 0, 0, 0)
        layoutForm.setSpacing(10)

        if label == "Fitness Goal":
            inputField = QComboBox()
            inputField.addItem("Select Goal")
            goals = [
                "weight_loss",
                "muscle_gain",
                "fat_loss",
                "rehabilitation",
                "toning",
                "maintain_weight",
                "flexibility",
                "strength",
                "endurance",
                "mobility",
                "posture",
                "mental_health",
                "general_health"
            ]
            inputField.addItems(goals)
        
            self.inputFields[label] = inputField
        else:
            inputField = QLineEdit()
            if label == "Height" or label == "Weight" or label == "Age":
                validator = QIntValidator()
                inputField.setValidator(validator)
            content = str(content) if isinstance(content,int) else content
            content = str(content) if isinstance(content,float) else content
            inputField.setText(content)
            inputField.setStyleSheet("""
            QLineEdit {
                border: 2px solid #2980b9;
                border-radius: 5px;
                padding: 5px;
                background-color: #f9f9f9;
                color: #2c3e50;
            }
            QLineEdit:focus {
                border: 2px solid #1abc9c;
                background-color: #ffffff;
                color: #2c3e50;
            }
            """)
            self.inputFields[label] = inputField

        textlabel = QLabel(label.ljust(12) + ":")
        layoutForm.addWidget(textlabel)
        layoutForm.addWidget(inputField)
        if label == "Weight":
            unit = QLabel("Kg")
            layoutForm.addWidget(unit)
        elif label == "Height":
            unit = QLabel("Cm")
            layoutForm.addWidget(unit)

        formContainer.setLayout(layoutForm)

        return formContainer

    def confirmChanges(self):
        # Validasi input sebelum menyimpan perubahan
        updated_data = {}
        for label in self.labels:
            if label[1] == "Fitness Goal":
                new_value = self.inputFields[label[1]].currentText()
            else:
                new_value = self.inputFields[label[1]].text().strip()

            # Tampilkan pop-up jika input kosong
            if label[1] == "Fitness Goal" and new_value == "Select Goal":
                self.showWarningPopup(f"{label[1]} Select goal first.")
                return
            elif label[1] == "Age":
                if int(new_value) <= 0:
                    self.showWarningPopup(f"{label[1]} cannot lower than 0.")
                    return;
                elif int(new_value) > 99:
                    self.showWarningPopup(f"{label[1]} cannot higher than 99.")
                    return;
            elif label[1] == "Height":
                if int(new_value) <= 0:
                    self.showWarningPopup(f"{label[1]} cannot lower than 0.")
                    return;
                elif int(new_value) >= 350:
                    self.showWarningPopup(f"{label[1]} cannot higher than 350.")
                    return;
            elif label[1] == "Weight":
                if int(new_value) <= 0:
                    self.showWarningPopup(f"{label[1]} cannot lower than 0.")
                    return;
                elif int(new_value) >= 350:
                    self.showWarningPopup(f"{label[1]} cannot higher than 350.")
                    return;
    
    
            if not new_value:
                self.showWarningPopup(f"{label[1]} cannot be empty.")
                return

            updated_data[label[0]] = new_value

        # Update data di controller
        self.controller.update_profile_data(updated_data)

        # Sinkronkan data lokal dengan yang di controller
        self.profile_data = self.controller.get_profile_data()

        # Update tampilan untuk mencerminkan data baru
        for i, label in enumerate(self.labels):
            container = self.profileLayout.itemAt(i).widget()

            if label[1] == "Weight":
                text = f"{label[1].ljust(12)}:   {self.profile_data[label[0]]} Kg"
            elif label[1] == "Height":
                text = f"{label[1].ljust(12)}:   {self.profile_data[label[0]]} Cm"
            else:
                text = f"{label[1].ljust(12)}:   {self.profile_data[label[0]]}"
            container.layout().itemAt(0).widget().setText(text)

        # Kembali ke mode tampilan
        self.sidebar.refresh_name(self.profile_data['nama'])
        self.home.refresh_name(self.profile_data['nama'])

        self.toggleEditMode()

    def showWarningPopup(self, message):
        msgBox = QMessageBox(self)
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setWindowTitle("Warning")
        msgBox.setText(message)
        msgBox.setStyleSheet("""
            QMessageBox {
                background-color: #f5f5f5;
                color: #2c3e50;
                font-family: Arial;
                font-size: 14px;
            }
            QMessageBox QLabel {
                font-weight: bold;
            }
            QMessageBox QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 5px;
                font-size: 12px;
            }
            QMessageBox QPushButton:hover {
                background-color: #5dade2;
            }
        """)
        msgBox.exec_()

    def discardChanges(self):
        self.toggleEditMode()
