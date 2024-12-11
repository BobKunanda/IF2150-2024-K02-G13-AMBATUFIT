import sys
import os
from PyQt5.QtWidgets import QMessageBox,QGraphicsDropShadowEffect, QTextEdit, QVBoxLayout,QSpacerItem, QSizePolicy, QHBoxLayout, QWidget, QPushButton, QLabel, QStackedLayout, QLineEdit
from PyQt5.QtCore import Qt, QPropertyAnimation, QSize, QTimer
from PyQt5.QtGui import QColor, QPalette, QIcon, QFont,QIntValidator
from backend.controllers.FitnessAdviceController import FitnessAdviceController

class FitnessAdvice(QWidget):
    def __init__(self, db_filename):
        super().__init__()
        self.controller = FitnessAdviceController(db_filename)  
        self.initUI()

    def initUI(self):
        self.fitness_advice_data = self.controller.get_fitness_advice_data()