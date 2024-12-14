import sys
import os
from PyQt5.QtWidgets import (QMessageBox, QGraphicsDropShadowEffect, QVBoxLayout, 
                             QHBoxLayout, QWidget, QPushButton, QLabel, 
                             QScrollArea, QSizePolicy, QDialog, QFormLayout, QDialogButtonBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from src.backend.controllers.SaranKebugaranController import SaranKebugaranController

class SaranKebugaranWidget(QWidget):
    def __init__(self, db_filename):
        super().__init__()
        self.controller = SaranKebugaranController(db_filename)
        self.initUI()

    def initUI(self):
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(30)

        # Title label for the whole section
        self.titleLabel = QLabel("Fitness Advice")
        self.titleLabel.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
            }
        """)
        self.titleLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        mainLayout.addWidget(self.titleLabel)

        # Create two "cards" with Saran Kebugaran titles
        try:
            if (self.controller.get_corresponding_saran_kebugaran() == None):
                saran_latihan = "Data profil belum diisi"
                saran_nutrisi = "Data profil belum diisi"
            else:
                saran_data = self.controller.get_corresponding_saran_kebugaran()
                saran_latihan = saran_data["saran_latihan"]
                saran_nutrisi = saran_data["saran_nutrisi"]

            # Create two "cards" with the saran kebugaran titles and descriptions
            saran1Container = self.createCard("Saran Latihan", saran_latihan)
            saran2Container = self.createCard("Saran Nutrisi", saran_nutrisi)

            mainLayout.addWidget(saran1Container)
            mainLayout.addWidget(saran2Container)
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

        # Scroll area for the content
        scrollArea = QScrollArea()
        scrollWidget = QWidget()
        scrollWidget.setLayout(mainLayout)
        scrollArea.setWidget(scrollWidget)
        scrollArea.setWidgetResizable(True)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(scrollArea)

    def createCard(self, title, description):
        cardContainer = QWidget()
        layoutForm = QVBoxLayout()
        layoutForm.setContentsMargins(20, 20, 20, 20)
        layoutForm.setSpacing(10)

        # Create the card's content
        titleLabel = QLabel(f"<b>{title}</b>")
        descriptionLabel = QLabel(description)

        # Styling the content
        titleLabel.setAlignment(Qt.AlignCenter)
        descriptionLabel.setAlignment(Qt.AlignCenter)

        # Set styles for the labels
        titleLabel.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #2c3e50;
                padding: 5px 0;
            }
        """)
        descriptionLabel.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #34495e;
                padding: 5px 0;
            }
        """)

        layoutForm.addWidget(titleLabel)
        layoutForm.addWidget(descriptionLabel)

        # Button layout for each card
        buttonsLayout = QVBoxLayout()
        layoutForm.addLayout(buttonsLayout)

        # Card Styling
        cardContainer.setLayout(layoutForm)
        cardContainer.setStyleSheet("""
            QWidget {
                border-radius: 10px;
                background-color: #ecf0f1;
                border: 1px solid #bdc3c7;
                padding: 15px;
            }
            QWidget:hover {
                background-color: #dfe6e9;
                border: 1px solid #2980b9;
            }
        """)
        cardContainer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(15)
        shadow_effect.setOffset(0, 4)
        shadow_effect.setColor(QColor(0, 0, 0, 100))
        cardContainer.setGraphicsEffect(shadow_effect)

        return cardContainer