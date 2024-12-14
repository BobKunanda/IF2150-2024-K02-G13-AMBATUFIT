import sys
from PyQt5.QtWidgets import (
    QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox, QDialog, QListWidget,
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
        self.exercise_scheme_data = []

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
        self.edit_card = self.edit_exercise_card()
        self.content_stack.addWidget(self.edit_card)

        self.setLayout(main_layout)

    def exercise_list_card(self):
        """Creates the main exercise list view with a scrollable layout."""
        widget = QWidget()
        layout = QVBoxLayout()

        # Scrollable Area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        exercise_container = QWidget()
        self.exercise_scheme_layout = QVBoxLayout()
        self.exercise_scheme_layout.setAlignment(Qt.AlignTop)
        exercise_container.setLayout(self.exercise_scheme_layout)
        scroll_area.setWidget(exercise_container)
        scroll_area.setStyleSheet("border: none;")
        layout.addWidget(scroll_area)

        # Add Default "Back Day" Card
        #self.add_exercise_card("Back Day", "Duration: 30 min    Type: Strength Training", "Description", [("Push-ups", 15), ("Pull-ups", 10), ("Sit-ups", 10), ("Looks-Maxxing", 10) , ("Mewing", 25)])

        # Floating Add Button
        add_button = QPushButton("+")
        add_button.setStyleSheet(
            """
            QPushButton {
                background-color: #2E3B55;
                color: white;
                font-size: 20px;
                border-radius: 25px;
                width: 50px;
                height: 50px;
            }
            QPushButton:hover {
                background-color: #405372;
            }
            """
        )
        add_button.setFixedSize(50, 50)
        add_button.clicked.connect(self.add_new_exercise_scheme)
        layout.addWidget(add_button, alignment=Qt.AlignRight | Qt.AlignBottom)

        widget.setLayout(layout)
        return widget
            
    def content_exercise_card(self, title, info, description, exercise_list):
        """Creates a detailed view for a specific exercise."""
        card = QFrame()
        card.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border-radius: 30px;
                border: 1px solid #DDDDDD;
            }
            """
        )
        card.setFixedHeight(400)  # Adjust height for better appearance

        layout = QVBoxLayout()
        title_layout = QHBoxLayout()

        # Title
        self.card_title = QLabel(f"{title}")
        self.card_title.setFont(QFont("Inter", 36, QFont.Bold))
        self.card_title.setStyleSheet("color: #2F3A59; border: none;")
        title_layout.addWidget(self.card_title)
        title_layout.addStretch()

        # Edit Button
        edit_button = QPushButton("Edit Training")
        edit_button.setFont(QFont("Inter", 12))
        edit_button.setStyleSheet(
            """
            QPushButton {
                background-color: #2E3B55;
                color: white;
                padding: 5px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #405372;
            }
            """
        )
        edit_button.setFixedWidth(150)
        edit_button.clicked.connect(lambda: self.content_stack.setCurrentIndex(2))
        title_layout.addWidget(edit_button, alignment=Qt.AlignRight)
        layout.addLayout(title_layout)

        # Info
        self.card_info = QLabel(info)
        self.card_info.setFont(QFont("Inter", 16))
        self.card_info.setStyleSheet("color: #555555; border: none;")
        layout.addWidget(self.card_info)

        # Description
        self.card_description = QLabel(description)
        self.card_description.setFont(QFont("Inter", 16))
        self.card_description.setStyleSheet("color: #777777; border: none;")
        self.card_description.setWordWrap(True)
        layout.addWidget(self.card_description)

        # Exercise List
        self.exercise_list_widget = QListWidget()
        for exercise in exercise_list:
            # Format exercise details excluding the ID
            exercise_details = f"Name: {exercise[1]}, Reps: {exercise[2]}, Sets: {exercise[3]}"
            self.exercise_list_widget.addItem(exercise_details)
        self.exercise_list_widget.setFont(QFont("Inter", 14))
        self.exercise_list_widget.setStyleSheet("color: #555555; border: none;")
        layout.addWidget(self.exercise_list_widget)

        # Scrollable Exercise List
        scroll_area = QScrollArea()
        scroll_area.setStyleSheet("border: none;")
        scroll_area.setWidgetResizable(True)

        exercise_list_container = QWidget()
        self.exercise_scheme_list_layout = QVBoxLayout()
        exercise_list_container.setLayout(self.exercise_scheme_list_layout)
        scroll_area.setWidget(exercise_list_container)

        layout.addWidget(scroll_area)
        
        # Back Button
        back_button = QPushButton("Back")
        back_button.setFont(QFont("Inter", 12))
        back_button.setStyleSheet(
            """
            QPushButton {
                background-color: #2E3B55;
                color: white;
                padding: 5px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #405372;
            }
            """
        )
        back_button.setFixedWidth(150)
        back_button.clicked.connect(lambda: self.content_stack.setCurrentIndex(0))
        layout.addWidget(back_button, alignment=Qt.AlignCenter)

        card.setLayout(layout)
        return card

    def update_content_card(self, title, info, description, exercises):
        """Updates the detailed content exercise card."""
        self.card_title.setText(title)
        self.card_info.setText(info)
        self.card_description.setText(description)

        # Update exercise list
        for i in reversed(range(self.exercise_scheme_list_layout.count())):
            self.exercise_scheme_list_layout.itemAt(i).widget().deleteLater()

        for exercise, reps in exercises:
            exercise_label = QLabel(f"{exercise} : {reps} reps")
            exercise_label.setFont(QFont("Inter", 14))
            exercise_label.setStyleSheet("color: #555555; border: none;")
            self.exercise_scheme_list_layout.addWidget(exercise_label)

    def add_exercise_scheme_card(self, title, info, description, exercises):
        """Adds a new exercise card to the scrollable layout."""
        card_data = (title, info, description, exercises)
        self.exercise_scheme_data.append((card_data))

        card = QFrame()
        card.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border-radius: 30px;
                border: 1px solid #DDDDDD;
            }
            """
        )
        card.setFixedHeight(400)

        layout = QVBoxLayout()
        title_layout = QHBoxLayout()

        # Title
        card_title = QLabel(f"{title}")
        card_title.setFont(QFont("Inter", 36, QFont.Bold))
        card_title.setStyleSheet("color: #2F3A59; border: none;")
        title_layout.addWidget(card_title)
        title_layout.addStretch()

        # Delete Button
        delete_button = QPushButton("Delete Training")
        delete_button.setFont(QFont("Inter", 12))
        delete_button.setStyleSheet(
            """
            QPushButton {
                background-color: red;
                color: white;
                padding: 5px 25px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #8B0000;
            }
            """
        )
        delete_button.setFixedWidth(200)
        delete_button.clicked.connect(lambda: self.confirm_deletion(card, card_data))
        title_layout.addWidget(delete_button, alignment=Qt.AlignRight)

        layout.addLayout(title_layout)

        # Info
        card_info = QLabel(f"{info}")
        card_info.setFont(QFont("Inter", 16))
        card_info.setStyleSheet("color: #555555; border: none;")
        layout.addWidget(card_info)

        # Description
        card_description = QLabel(f"{description}")
        card_description.setFont(QFont("Inter", 16))
        card_description.setStyleSheet("color: #555555; border: none;")
        layout.addWidget(card_description)

        # Dropdown Button
        info_button = QPushButton("Info Training")
        info_button.setFont(QFont("Inter", 12))
        info_button.setStyleSheet(
            """
            QPushButton {
                background-color: #2E3B55;
                color: white;
                padding: 5px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #405372;
            }
            """
        )
        info_button.setFixedWidth(200)
        info_button.setFixedHeight(30)
        info_button.clicked.connect(lambda: self.show_exercise_details(title, info, description, exercises))
        layout.addWidget(info_button, alignment=Qt.AlignCenter)

        card.setLayout(layout)
        self.exercise_scheme_layout.addWidget(card)
    
    def add_exercise_card(self, exercise, reps, sets):
        """Adds a new exercise card to the scrollable layout."""
        card_data = (exercise, reps, sets)
        self.exercise_scheme_data.append((card_data))

        card = QFrame()
        card.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border-radius: 30px;
                border: 1px solid #DDDDDD;
            }
            """
        )
        card.setFixedHeight(100)

        layout = QVBoxLayout()
        title_layout = QHBoxLayout()

        # Info
        card_info = QLabel(f"{exercise}", f"{reps}", f"{sets}")
        card_info.setFont(QFont("Inter", 16))
        card_info.setStyleSheet("color: #555555; border: none;")
        layout.addWidget(card_info)

        # Delete Button
        delete_button = QPushButton("Delete Exercise")
        delete_button.setFont(QFont("Inter", 12))
        delete_button.setStyleSheet(
            """
            QPushButton {
                background-color: red;
                color: white;
                padding: 5px 25px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #8B0000;
            }
            """
        )
        delete_button.setFixedWidth(200)
        delete_button.clicked.connect(lambda: self.confirm_deletion(card, card_data))
        title_layout.addWidget(delete_button, alignment=Qt.AlignRight)

        layout.addLayout(title_layout)

       
    def edit_exercise_card(self):
        """Creates the edit exercise card."""
        card = QWidget()
        layout = QVBoxLayout()

        # Title Input
        self.edit_title = QLineEdit()
        self.edit_title.setPlaceholderText("Title")
        self.edit_title.setFont(QFont("Inter", 16))
        self.edit_title.setStyleSheet("padding: 10px; border: 1px solid #DDDDDD; border-radius: 5px;")
        layout.addWidget(self.edit_title)

        # Duration Dropdown
        self.edit_duration = QComboBox()
        self.edit_duration.addItems([f"{i} min" for i in range(15, 65, 5)])
        self.edit_duration.setFont(QFont("Inter", 16))
        self.edit_duration.setStyleSheet("padding: 10px; border: 1px solid #DDDDDD; border-radius: 5px;")
        layout.addWidget(self.edit_duration)

        # Type Dropdown
        self.edit_type = QComboBox()
        exercise_types = ["Strength", "Endurance", "Speed", "Flexibility", "Balance"]
        self.edit_type.addItems(exercise_types)
        self.edit_type.setFont(QFont("Inter", 16))
        self.edit_type.setStyleSheet("padding: 10px; border: 1px solid #DDDDDD; border-radius: 5px;")
        layout.addWidget(self.edit_type)

        # Description Input
        self.edit_description = QTextEdit()
        self.edit_description.setPlaceholderText("Description")
        self.edit_description.setFont(QFont("Inter", 16))
        self.edit_description.setStyleSheet("padding: 10px; border: 1px solid #DDDDDD; border-radius: 5px;")
        self.edit_description.setFixedHeight(100)
        layout.addWidget(self.edit_description)

        # Scrollable Exercise List
        scroll_area = QScrollArea()
        scroll_area.setStyleSheet("border: none;")
        scroll_area.setWidgetResizable(True)
        exercise_list_container = QWidget()
        self.exercise_list_layout = QVBoxLayout()
        exercise_list_container.setLayout(self.exercise_list_layout)
        scroll_area.setWidget(exercise_list_container)

        layout.addWidget(scroll_area)

        add_button = QPushButton("Add Exercise")
        add_button.setStyleSheet(
            """
            QPushButton {
                background-color: #2E3B55;
                color: white;
                font-size: 16px;
                padding: 10px;
                border: 1px solid #2E3B55;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #405372;
            }
            """
        )
        add_button.setFixedHeight(50)
        add_button.clicked.connect(self.show_exercise_input_dialog)
        layout.addWidget(add_button, alignment=Qt.AlignRight | Qt.AlignBottom)


        # Save Button
        save_button = QPushButton("Save")
        save_button.setFont(QFont("Inter", 12))
        save_button.setStyleSheet(
            """
            QPushButton {
                background-color: #2E3B55;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #405372;
            }
            """
        )
        save_button.clicked.connect(self.confirm_save)
        layout.addWidget(save_button, alignment=Qt.AlignRight)

        # Back Button
        back_button = QPushButton("Cancel")
        back_button.setFont(QFont("Inter", 12))
        back_button.setStyleSheet(
            """
            QPushButton {
                background-color: #DDDDDD;
                color: black;
                padding: 10px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #CCCCCC;
            }
            """
        )
        back_button.clicked.connect(lambda: self.content_stack.setCurrentIndex(1))
        layout.addWidget(back_button, alignment=Qt.AlignLeft)

        card.setLayout(layout)
        return card


    def switch_to_edit_card(self, title, info, description):
        """Populates the edit card with current details and switches to it."""
        self.edit_title.setText(title)
        if info:
            duration, exercise_type = info.split("    Type: ")
            self.edit_duration.setCurrentText(duration.replace("Duration: ", ""))
            self.edit_type.setCurrentText(exercise_type)
        self.edit_description.setText(description)
        self.content_stack.setCurrentIndex(2)

    def save_exercise_scheme_details(self):
        """Saves the edited details back to the exercise and switches to the info card."""
        new_title = self.edit_title.text()
        new_duration = self.edit_duration.currentText()
        new_type = self.edit_type.currentText()
        new_info = f"Duration: {new_duration}    Type: {new_type}"
        new_description = self.edit_description.toPlainText()

        self.card_title.setText(new_title)
        self.card_info.setText(new_info)
        self.card_description.setText(new_description)
    
    def save_exercise_details(self):
        """Saves the edited details back to the exercise and switches to the info card."""
        new_exercise = self.edit_exercise.currentText()
        new_reps = self.edit_reps.currentText()
        new_sets = self.edit_sets.currentText()

        self.card_exercise.setText(new_exercise)
        self.card_reps.setText(new_reps)
        self.card_sets.setText(new_sets)

    def show_exercise_details(self, title, info, description, exercises):
        """Shows the details of a specific exercise card."""
        self.update_content_card(title, info, description, exercises)
        self.content_stack.setCurrentIndex(1)

    def add_new_exercise_scheme(self):
        """Adds a dynamically created exercise card."""
        count = self.exercise_scheme_layout.count() + 1
        self.add_exercise_scheme_card(f"Exercise {count}", "Duration: -    Type: -", "-", [("-", 0)])

    def add_new_exercise(self):
        count = self.exercise_layout.count() + 1
        self.add_exercise_card(f"Exercise {count}", "Duration: -    Type: -", "-", [("-", 0)])


    def confirm_deletion(self, card, card_data):
        reply = QMessageBox.question(self, 'Confirm Deletion', 'Are you sure you want to delete this training?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.exercise_scheme_layout.removeWidget(card)
            card.deleteLater()
            if card_data in self.exercise_scheme_data:
                self.exercise_scheme_data.remove(card_data)

    def confirm_save(self):
        reply = QMessageBox.question(self, 'Confirm Save', 'Are you sure you want to save this?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.save_exercise_scheme_details
            self.content_stack.setCurrentIndex(1)

    def show_exercise_input_dialog(self):
        """Shows a dialog to input exercise details."""
        # Create a QDialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Exercise Details")
        dialog.setModal(True)
        dialog_layout = QVBoxLayout(dialog)

        # Exercise Dropdown
        exercise_label = QLabel("Select Exercise:")
        self.edit_exercise = QComboBox()
        self.edit_exercise.addItems(["Push-ups", "Pull-ups", "Sit-ups", "Squats", "Lunges"])  # Example exercises
        dialog_layout.addWidget(exercise_label)
        dialog_layout.addWidget(self.edit_exercise)

        # Reps Dropdown
        reps_label = QLabel("Select Repetitions:")
        self.edit_reps = QComboBox()
        self.edit_reps.addItems([str(i) for i in range(1, 30)])  # Reps from 1 to 30
        dialog_layout.addWidget(reps_label)
        dialog_layout.addWidget(self.edit_reps)

        # Sets Dropdown
        sets_label = QLabel("Select Sets:")
        self.edit_sets = QComboBox()
        self.edit_sets.addItems([str(i) for i in range(1, 6)])  # Sets from 1 to 5
        dialog_layout.addWidget(sets_label)
        dialog_layout.addWidget(self.edit_sets)

        # Buttons for Confirm and Cancel
        button_layout = QHBoxLayout()
        confirm_button = QPushButton("Confirm")
        confirm_button.clicked.connect(self.save_exercise_details)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(dialog.reject)
        button_layout.addWidget(confirm_button)
        button_layout.addWidget(cancel_button)
        dialog_layout.addLayout(button_layout)

        dialog.exec() 
    

            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Exercise()
    window.show()
    sys.exit(app.exec_())
