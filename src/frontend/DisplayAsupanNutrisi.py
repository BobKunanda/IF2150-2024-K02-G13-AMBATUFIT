import sys
import os
from datetime import datetime as dt
from PyQt5.QtWidgets import (QMessageBox, QGraphicsDropShadowEffect, QVBoxLayout, QHBoxLayout, 
                             QWidget, QPushButton, QLabel, QStackedLayout, QLineEdit, QSpacerItem, 
                             QSizePolicy, QTextEdit, QScrollArea, QDialog, QFormLayout, QDialogButtonBox)
from PyQt5.QtCore import Qt, QSize, QDateTime
from PyQt5.QtGui import QColor, QIcon, QIntValidator
from backend.controllers.AsupanNutrisiController import AsupanNutrisiController
from backend.models import AsupanNutrisi

class AsupanNutrisiWidget(QWidget):
    def __init__(self, db_filename):
        super().__init__()
        self.controller = AsupanNutrisiController(db_filename)
        self.initUI()

    def initUI(self):
        self.asupan_data = self.controller.get_all_asupan()
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(30)

        # Create title label
        self.titleLabel = QLabel("Asupan Nutrisi")
        self.titleLabel.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
            }
        """)
        self.titleLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        mainLayout.addWidget(self.titleLabel)

        # Create "Add" button
        self.addButton = QPushButton("Add New Nutritional Intake")
        self.addButton.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border-radius: 5px;
                font-size: 14px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        self.addButton.clicked.connect(self.showAddDialog)
        mainLayout.addWidget(self.addButton)

        # Create form containers (cards)
        for row in self.asupan_data:
            name = row[1] if len(row) > 1 else "N/A"
            datetime = row[2] if len(row) > 2 else "N/A"
            karbo = row[3] if len(row) > 3 else 0
            protein = row[4] if len(row) > 4 else 0
            lemak = row[5] if len(row) > 5 else 0
            mineral = row[6] if len(row) > 5 else 0
            air = row[7] if len(row) > 5 else 0
            asupan_id = row[0]  # Get the unique ID of the asupan

            container = self.createForm(asupan_id, name, datetime, karbo, protein, lemak, mineral, air)
            mainLayout.addWidget(container)

        # Create scroll area
        scrollArea = QScrollArea()
        scrollWidget = QWidget()
        scrollWidget.setLayout(mainLayout)
        scrollArea.setWidget(scrollWidget)
        scrollArea.setWidgetResizable(True)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(scrollArea)

    def resetUI(self):
        for i in reversed(range(self.layout().count())):
            self.layout().itemAt(i).widget().deleteLater()
        self.initUI()
        

    def createForm(self, asupan_id, name, datetime, karbo, protein, lemak, mineral, air):
        formContainer = QWidget()
        layoutForm = QVBoxLayout()
        layoutForm.setContentsMargins(20, 20, 20, 20)
        layoutForm.setSpacing(10)

        # Content (Labels)
        contentLayout = QVBoxLayout()
        titleLabel = QLabel(f"<b>{name}</b>")
        datetime = dt.strftime(datetime, "%Y/%m/%d %H:%M")
        datetimeLabel = QLabel(f"Date/Time: {datetime}")
        karboLabel = QLabel(f"Karbohidrat: {karbo}g")
        proteinLabel = QLabel(f"Protein: {protein}g")
        lemakLabel = QLabel(f"Lemak: {lemak}g")
        mineralLabel = QLabel(f"Mineral: {mineral}g")
        airLabel = QLabel(f"Air: {air}ml")

        # Styling labels
        labels = [titleLabel, datetimeLabel, karboLabel, proteinLabel, lemakLabel, mineralLabel, airLabel]
        for label in labels:
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    color: #34495e;
                    padding: 5px 0;
                }
            """)

        for label in labels:
            contentLayout.addWidget(label)

        layoutForm.addLayout(contentLayout)

        # Button Layout (specific to each card)
        buttonsLayout = QVBoxLayout()

        # Store the asupan_id in the form container
        formContainer.asupan_id = asupan_id
        formContainer.name = name
        formContainer.buttonsLayout = buttonsLayout  # Store buttonsLayout in the container

        # Create the "Edit" button and connect to the popup function
        editButton = QPushButton("Edit")
        editButton.setStyleSheet("""
            QPushButton {
                background-color: #2980b9;
                color: white;
                border-radius: 5px;
                font-size: 14px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #3498db;
            }
        """)
        editButton.clicked.connect(lambda: self.showEditDialog(formContainer, name, karbo, protein, lemak, mineral, air))

        buttonsLayout.addWidget(editButton)

        # Create the "Delete" button
        deleteButton = QPushButton("Delete")
        deleteButton.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border-radius: 5px;
                font-size: 14px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        deleteButton.clicked.connect(lambda: self.deleteAsupan(formContainer))

        buttonsLayout.addWidget(deleteButton)

        layoutForm.addLayout(buttonsLayout)

        # Card Styling
        formContainer.setLayout(layoutForm)
        formContainer.setStyleSheet("""
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
        formContainer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(15)
        shadow_effect.setOffset(0, 4)
        shadow_effect.setColor(QColor(0, 0, 0, 100))
        formContainer.setGraphicsEffect(shadow_effect)

        return formContainer

    def showAddDialog(self):
        """Show the add dialog to input data for new Asupan Nutrisi."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Nutrisi")
        dialog.setFixedSize(400, 300)

        formLayout = QFormLayout()

        # LineEdit for inputting values
        nameEdit = QLineEdit(self)
        formLayout.addRow("Nama asupan:", nameEdit)

        karboEdit = QLineEdit(self)
        formLayout.addRow("Karbohidrat (g):", karboEdit)

        proteinEdit = QLineEdit(self)
        formLayout.addRow("Protein (g):", proteinEdit)

        lemakEdit = QLineEdit(self)
        formLayout.addRow("Lemak (g):", lemakEdit)

        mineralEdit = QLineEdit(self)
        formLayout.addRow("Mineral (g):", mineralEdit)

        airEdit = QLineEdit(self)
        formLayout.addRow("Air (ml):", airEdit)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(lambda: self.onAddAccepted(nameEdit, karboEdit, proteinEdit, lemakEdit, mineralEdit, airEdit, dialog))
        buttonBox.rejected.connect(dialog.reject)

        formLayout.addWidget(buttonBox)
        dialog.setLayout(formLayout)
        dialog.exec_()


    def showEditDialog(self, formContainer, name, karbo, protein, lemak, mineral, air):
        """Menampilkan dialog edit untuk mengubah data asupan nutrisi."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Nutrisi")
        dialog.setFixedSize(400, 300)

        formLayout = QFormLayout()

        # LineEdit buat input nutrisi
        nameEdit = QLineEdit(self)
        nameEdit.setText(name)
        formLayout.addRow("Nama asupan:", nameEdit)

        karboEdit = QLineEdit(self)
        karboEdit.setText(str(karbo))
        formLayout.addRow("Karbohidrat (g):", karboEdit)

        proteinEdit = QLineEdit(self)
        proteinEdit.setText(str(protein))
        formLayout.addRow("Protein (g):", proteinEdit)

        lemakEdit = QLineEdit(self)
        lemakEdit.setText(str(lemak))
        formLayout.addRow("Lemak (g):", lemakEdit)

        mineralEdit = QLineEdit(self)
        mineralEdit.setText(str(mineral))
        formLayout.addRow("Mineral (g):", mineralEdit)

        airEdit = QLineEdit(self)
        airEdit.setText(str(air))
        formLayout.addRow("Air (ml):", airEdit)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(lambda: self.onEditAccepted(nameEdit, karboEdit, proteinEdit, lemakEdit, mineralEdit, airEdit, formContainer, dialog))
        buttonBox.rejected.connect(dialog.reject)

        formLayout.addWidget(buttonBox)
        dialog.setLayout(formLayout)
        dialog.exec_()

    def onAddAccepted(self, nameEdit, karboEdit, proteinEdit, lemakEdit, mineralEdit, airEdit, dialog):
        # Mendapatkan input dari user
        name = nameEdit.text()
        karbo = "0.0" if karboEdit.text() == "" else karboEdit.text()
        protein = "0.0" if proteinEdit.text() == "" else proteinEdit.text()
        lemak = "0.0" if lemakEdit.text() == "" else lemakEdit.text()
        mineral = "0.0" if mineralEdit.text() == "" else mineralEdit.text()
        air = "0.0" if airEdit.text() == "" else airEdit.text()
        
        # Cek apakah nama asupan kosong
        if nameEdit.text() == "":
            QMessageBox.warning(self, "Invalid Input", "Mohon masukkan nama asupan.")
            dialog.exec_()
            return
        try:
            # Cek apakah input valid
            karbo = float(karbo)
            protein = float(protein)
            lemak = float(lemak)
            mineral = float(mineral)
            air = float(air)
        except ValueError:
            # Kalo input gak valid, tampilkan pesan error
            QMessageBox.warning(self, "Invalid Input", "Mohon masukkan input yang valid berupa bilangan desimal.")
            dialog.exec_()
            return

        # Mendapatkan timestamp sekarang
        datetime = dt.now().strftime("%Y/%m/%d %H:%M")
        
        # Menambahkan asupan nutrisi ke database
        nutrients = {1: karbo, 2: protein, 3: lemak, 4: mineral, 5: air}        
        self.controller.add_asupan_nutrisi(name, datetime, nutrients)

        # Reset UI
        self.resetUI()
        dialog.accept()

    def onEditAccepted(self, nameEdit, karboEdit, proteinEdit, lemakEdit, mineralEdit, airEdit, formContainer, dialog):
        # Mendapatkan input dari user
        name = nameEdit.text()
        karbo = karboEdit.text()
        protein = proteinEdit.text()
        lemak = lemakEdit.text()
        mineral = mineralEdit.text()
        air = airEdit.text()

        try:
            # Cek apakah input valid
            float(karbo)
            float(protein)
            float(lemak)
            float(mineral)
            float(air)
        except ValueError:
            # Kalo input gak valid, tampilkan pesan error
            QMessageBox.warning(self, "Invalid Input", "Mohon masukkan input yang valid berupa bilangan desimal.")
            dialog.exec_()
            return

        # print(f"Berhasil mengubah Asupan ID {formContainer.asupan_id}: Nama={name}, karbo={karbo}, Protein={protein}, lemak={lemak}, mineral={mineral}, air={air}") #Legacy code buat ngedebug
        karbo = float(karbo)
        protein = float(protein)
        lemak = float(lemak)
        mineral = float(mineral)
        air = float(air)

        # Update asupan nutrisi di database
        nutrients = {1: karbo, 2: protein, 3: lemak, 4: mineral, 5: air}
        # print(f"Updating Asupan ID {formContainer.asupan_id} with: {nutrients}") #Legacy code buat ngedebug
        self.controller.update_asupan_nutrisi(formContainer.asupan_id, name, nutrients)

        # Reset UI
        self.resetUI()
        dialog.accept()

    def deleteAsupan(self, formContainer):
        # Mendapatkan asupan_id dan nama asupan
        asupan_id = formContainer.asupan_id
        name = formContainer.name

        # Tampilkan dialog konfirmasi
        reply = QMessageBox.question(self, 'Confirm Deletion',
                                    f"Apakah Anda yakin ingin menghapus {name}?",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        # Kalo user menekan tombol Yes, hapus asupan
        if reply == QMessageBox.Yes:
            success = self.controller.delete_asupan_nutrisi(asupan_id)
            # Kalo berhasil menghapus, tampilkan pesan sukses
            if success:
                QMessageBox.information(self, "Deleted", f"{name} berhasil dihapus.")
                self.resetUI()
            # Kalo gagal menghapus, tampilkan pesan error
            else:
                QMessageBox.warning(self, "Error", "Gagal menghapus Asupan.")