import sys
from PyQt5.QtWidgets import (
    QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox,
    QLabel, QWidget, QFrame, QScrollArea, QStackedLayout, QLineEdit, QTextEdit, QComboBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon


class ExerciseData:
    def __init__(self, id, title, duration, type, description, exercise):
        self.id = id
        self.title = title
        self.duration = duration
        self.type = type
        self.description = description
        self.exercise = exercise

class ExerciseManager:
    def __init__(self):
        self.exercises = []
        self.next_id = 1  # Simple auto-increment mechanism for IDs

    def add_exercise(self, title, duration, type, description, exercises):
        new_exercise = ExerciseData(self.next_id, title, duration, type, description, exercises)
        self.exercises.append(new_exercise)
        self.next_id += 1
        return new_exercise

    def remove_exercise(self, id):
        self.exercises = [ex for ex in self.exercises if ex.id != id]

    def update_exercise(self, id, title, duration, type, description, exercises):
        for ex in self.exercises:
            if ex.id == id:
                ex.title = title
                ex.duration = duration
                ex.type = type
                ex.description = description
                ex.exercises = exercises
                return ex
        return None

    def get_exercises(self):
        for ex in self.exercises:
            if ex.id == id:
                return ex
        return None

class Exercise(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Ambatufit")
        self.setWindowIcon(QIcon("src/assets/icons/logo.jpg"))
        self.setGeometry(100, 100, 800, 600)

        # Data structure to store exercise details
        self.exercise_data = []

        # Main layout
        main_layout = QVBoxLayout()

        # Static Header
        header = QLabel("Exercise")
        header.setFont(QFont("Inter", 36, QFont.Bold))
        header.setStyleSheet("color: #2F3A59; padding: 20px;")
        header.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(header)

        # Content Area (Dynamic)
        self.content_stack = QStackedLayout()
        main_layout.addLayout(self.content_stack)

        # Initial Card
        initial_card = self.exercise_list_card()
        self.content_stack.addWidget(initial_card)

        # Info Card (Placeholder)
        self.info_card = self.content_exercise_card("", "", "", [])
        self.content_stack.addWidget(self.info_card)

        # Edit Card
        self.edit_card = self.edit_exercise_card(False)
        self.content_stack.addWidget(self.edit_card)

        # Add Card
        self.add_card = self.edit_exercise_card(True)
        self.content_stack.addWidget(self.add_card)
        self.setLayout(main_layout)
