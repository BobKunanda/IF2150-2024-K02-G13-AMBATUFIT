import sys
import os
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QTextEdit, QVBoxLayout,QSpacerItem, QSizePolicy, QHBoxLayout, QWidget, QPushButton, QLabel, QStackedLayout, QLineEdit
from PyQt5.QtCore import Qt, QPropertyAnimation, QSize, QTimer
from PyQt5.QtGui import QColor, QPalette, QIcon, QFont,QIntValidator

class Profile(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
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

        self.labels = ["Name", "Age", "Height", "Weight", "Fitness Goal"]
        self.profileData = ["John Doe", "30", 180, 80, "Lose 10 lbs"]
        self.inputFields = {}

        for i, label in enumerate(self.labels):
            container = self.createForm(label, self.profileData[i])
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
            container = self.createEditField(label, self.profileData[i])
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

       
        if label != "Fitness Goal":
            content = str(content) if isinstance(content,int) else content

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
        else:
            text = label.ljust(12) + ":"
            textlabel.setText(text)
            layoutForm.addWidget(textlabel)
            textlabel.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #34495e;
            }
            """)
            self.fitnessGoalWidget = QTextEdit()
            self.fitnessGoalWidget.setText(content)
            self.fitnessGoalWidget.setReadOnly(True)
            self.fitnessGoalWidget.setMaximumHeight(150)
            self.fitnessGoalWidget.setMinimumWidth(500)
            self.fitnessGoalWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.fitnessGoalWidget.setStyleSheet("""
                QTextEdit {
                    border: 2px solid #000000;
                    border-radius: 10px;  /* Rounded corners */
                    padding: 10px;        /* Adjust padding */
                    background-color: #f5f5f5;
                    font-size: 14px;
                    font-family: Arial, sans-serif;
                    color: #2c3e50;
                }
            """)

            # Apply drop shadow effect
            shadow_effect = QGraphicsDropShadowEffect()
            shadow_effect.setBlurRadius(12)  
            shadow_effect.setOffset(4, 4)  
            shadow_effect.setColor(QColor(0, 0, 0, 160)) 

            # Terapkan efek bayangan ke QTextEdit
            self.fitnessGoalWidget.setGraphicsEffect(shadow_effect)

            layoutForm.addWidget(self.fitnessGoalWidget, alignment=Qt.AlignTop)


        formContainer.setLayout(layoutForm)

        return formContainer

    def createEditField(self, label, content):
        formContainer = QWidget()
        layoutForm = QHBoxLayout()
        layoutForm.setContentsMargins(20, 0, 0, 0)
        layoutForm.setSpacing(10)

        if label == "Fitness Goal":
            layoutForm = QVBoxLayout() 
            layoutForm.setContentsMargins(20, 0, 0, 0)
            layoutForm.setSpacing(10)
            inputField = QTextEdit()
            inputField.setText(content)
            inputField.setMaximumHeight(150)
            inputField.setMinimumWidth(500)
            inputField.setStyleSheet("""
            QTextEdit {
                border: 2px solid #2980b9;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                font-family: Arial, sans-serif;
                background-color: #f9f9f9;
                color: #2c3e50;
            }
            QTextEdit:focus {
                border: 2px solid #1abc9c;
                background-color: #ffffff;
                color: #2c3e50;
            }
            """)
            self.inputFields[label] = inputField
        else:
            inputField = QLineEdit()
            if label == "Height" or label == "Weight" or label == "Age":
                # Apply QIntValidator to allow only integers (numbers)
                validator = QIntValidator()
                inputField.setValidator(validator)
            content = str(content) if isinstance(content,int) else content
            inputField.setText(content)
            inputField.setStyleSheet("""
            QLineEdit {
                border: 2px solid #2980b9;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
                font-family: Arial, sans-serif;
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

        for i, label in enumerate(self.labels):
            if label == "Fitness Goal":

                new_value = self.inputFields[label].toPlainText()
                self.profileData[i] = new_value  # Update data
                self.fitnessGoalWidget.setText(new_value) 
            else:
                new_value = self.inputFields[label].text()  
                self.profileData[i] = new_value  

        for i, label in enumerate(self.labels):
            container = self.profileLayout.itemAt(i).widget()
            if label != "Fitness Goal":
                if label == "Weight":
                    text = f"{label}:   {self.profileData[i]} Kg"
                elif label == "Height":
                    text = f"{label}:   {self.profileData[i]} Cm"
                else:
                    text = f"{label}:   {self.profileData[i]}"
                container.findChild(QLabel).setText(text)

        self.toggleEditMode()  

    def discardChanges(self):

        for i, label in enumerate(self.labels):
            if label == "Fitness Goal":

                self.fitnessGoalWidget.setText(self.profileData[i])
            else:
                # Pulihkan data asli pada QLabel
                container = self.profileLayout.itemAt(i).widget()
                text = f"{label}:   {self.profileData[i]}"
                container.findChild(QLabel).setText(text)

        self.toggleEditMode() 