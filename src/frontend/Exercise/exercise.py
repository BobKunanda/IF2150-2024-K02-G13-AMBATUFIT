import sys
from PyQt5.QtWidgets import (
    QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox, QListWidget, QDialog, QSpacerItem, QSizePolicy,
    QDialogButtonBox, QLabel, QWidget, QFrame, QScrollArea, QStackedLayout, QLineEdit, QTextEdit, QComboBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

class ExerciseData:
    def __init__(self, id, exercise_name, reps, sets):
        self.id = id
        self.exercise_name = exercise_name
        self.reps = reps
        self.sets = sets
        
class ExerciseSchemeData:
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
        new_exercise = ExerciseSchemeData(self.next_id, title, duration, type, description, exercises)
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

class Exercise(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ambatufit")
        self.setWindowIcon(QIcon("src/assets/icons/logo.jpg"))
        self.setGeometry(100, 100, 800, 600)
        self.exercise_manager = ExerciseManager()  # Initialize the exercise manager

        # Main layout
        main_layout = QVBoxLayout()

        # Static Header
        header = QLabel("Exercise")
        header.setFont(QFont("Inter", 36, QFont.Bold))
        header.setStyleSheet("color: #2F3A59; padding: 20px;")
        header.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(header)

        # Scrollable Area for Exercises
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        exercise_container = QWidget()
        self.exercise_scheme_layout = QVBoxLayout()
        self.exercise_scheme_layout.setAlignment(Qt.AlignTop)
        exercise_container.setLayout(self.exercise_scheme_layout)
        scroll_area.setWidget(exercise_container)
        scroll_area.setStyleSheet("border: none;")
        main_layout.addWidget(scroll_area)

        # Floating Add Button
        add_button = QPushButton("+")
        add_button.setStyleSheet("""
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
        """)
        add_button.setFixedSize(50, 50)
        add_button.clicked.connect(self.add_new_exercise_scheme)
        main_layout.addWidget(add_button, alignment=Qt.AlignRight | Qt.AlignBottom)

        self.setLayout(main_layout)

    def add_new_exercise_scheme(self):
        dialog = QDialog(self)
        dialog.setWindowTitle('Add New Exercise Scheme')
        layout = QVBoxLayout(dialog)

        # Title, Duration, Type, Description
        title_input = QLineEdit()
        duration_input = QComboBox()
        duration_input.addItems([f"{i} min" for i in range(15, 105, 5)])
        type_input = QComboBox()
        type_input.addItems(["Strength", "Endurance", "Speed", "Flexibility", "Balance"])
        description_input = QTextEdit()
        
        layout.addWidget(QLabel("Title"))
        layout.addWidget(title_input)
        layout.addWidget(QLabel("Duration"))
        layout.addWidget(duration_input)
        layout.addWidget(QLabel("Type"))
        layout.addWidget(type_input)
        layout.addWidget(QLabel("Description"))
        layout.addWidget(description_input)

        added_exercises = []
        exercise_details_layout = QVBoxLayout()

        # Exercise details with Add button
        exercise_input = QComboBox()
        exercise_input.addItems(["Push-ups", "Sit-ups", "Squats"])
        reps_input = QLineEdit()
        sets_input = QLineEdit()
        add_exercise_button = QPushButton("Add Exercise")

        def add_exercise_to_list():
            exercise = exercise_input.currentText()
            reps = reps_input.text()
            sets = sets_input.text()
            if not reps.isdigit() or not sets.isdigit():
                QMessageBox.warning(dialog, 'Invalid Input', 'Please enter valid numbers for reps and sets.')
                return
            if(len(added_exercises) == 0):
                id = 0
            else:
                id = added_exercises[-1].id + 1
            exercise_obj = ExerciseData(id, exercise, int(reps), int(sets))  # Create an Exercise object
            added_exercises.append(exercise_obj)  # Append the object
            exercise_details = QHBoxLayout()
            exercise_label = QLabel(f"{exercise} - Reps: {reps}, Sets: {sets}")
            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(lambda: delete_exercise(exercise_details, exercise_obj))

            exercise_details.addWidget(exercise_label)
            exercise_details.addWidget(delete_button)
            exercise_details_layout.addLayout(exercise_details)

            reps_input.clear()
            sets_input.clear()

        def delete_exercise(exercise_layout, exercise_obj):
            # Remove the layout first
            for i in reversed(range(exercise_layout.count())):
                widget = exercise_layout.itemAt(i).widget()
                if widget:
                    widget.deleteLater()
            exercise_layout.setParent(None)
            exercise_layout.deleteLater()

            # Now remove the corresponding exercise object from the list
            if exercise_obj in added_exercises:
                added_exercises.remove(exercise_obj)


        add_exercise_button.clicked.connect(add_exercise_to_list)

        layout.addLayout(exercise_details_layout)
        exercise_entry_layout = QHBoxLayout()
        exercise_entry_layout.addWidget(QLabel("Exercise"))
        exercise_entry_layout.addWidget(exercise_input)
        exercise_entry_layout.addWidget(QLabel("Reps"))
        exercise_entry_layout.addWidget(reps_input)
        exercise_entry_layout.addWidget(QLabel("Sets"))
        exercise_entry_layout.addWidget(sets_input)
        exercise_entry_layout.addWidget(add_exercise_button)

        layout.addLayout(exercise_entry_layout)

        # Dialog buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(lambda: self.accept_dialog(dialog, title_input, duration_input, type_input, description_input, added_exercises))
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        dialog.setLayout(layout)
        dialog.exec_()


    def edit_exercise_scheme(self, scheme):
        dialog = QDialog(self)
        dialog.setWindowTitle('Edit Exercise Scheme')
        layout = QVBoxLayout(dialog)

        # Title, Duration, Type, Description
        title_input = QLineEdit(scheme.title)
        duration_input = QComboBox()
        duration_input.addItems([f"{i} min" for i in range(15, 105, 5)])
        duration_input.setCurrentText(scheme.duration)
        type_input = QComboBox()
        type_input.addItems(["Strength", "Endurance", "Speed", "Flexibility", "Balance"])
        type_input.setCurrentText(scheme.type)
        description_input = QTextEdit(scheme.description)

        layout.addWidget(QLabel("Title"))
        layout.addWidget(title_input)
        layout.addWidget(QLabel("Duration"))
        layout.addWidget(duration_input)
        layout.addWidget(QLabel("Type"))
        layout.addWidget(type_input)
        layout.addWidget(QLabel("Description"))
        layout.addWidget(description_input)

        # Initialize list to store exercises
        added_exercises = [ExerciseData(ex.id, ex.exercise_name, ex.reps, ex.sets) for ex in scheme.exercise]
        exercise_details_layout = QVBoxLayout()

        # Exercise details with Add button
        exercise_input = QComboBox()
        exercise_input.addItems(["Push-ups", "Sit-ups", "Squats"])
        reps_input = QLineEdit()
        sets_input = QLineEdit()
        add_exercise_button = QPushButton("Add Exercise")
        
        def update_exercise_list():
            # Add each exercise with a delete button
            for ex in added_exercises:
                exercise_layout = QHBoxLayout()  # Create a horizontal layout for each exercise
                id = ex.id
                exercise = ex.exercise_name
                reps = ex.reps
                sets = ex.sets
                exercise_obj = ExerciseData(int(id), exercise, int(reps), int(sets))
                # Label showing the exercise details
                exercise_label = QLabel(f"{ex.exercise_name} - Reps: {ex.reps}, Sets: {ex.sets}")
                exercise_layout.addWidget(exercise_label)

                # Delete button for removing the exercise
                delete_button = QPushButton("Delete")
                delete_button.clicked.connect(lambda _, l=exercise_layout, obj=exercise_obj: delete_exercise(l, obj))

                exercise_layout.addWidget(delete_button)

                layout.addLayout(exercise_layout)  # Add the exercise layout to the main layout


        update_exercise_list()


        def add_exercise_to_list():
            exercise = exercise_input.currentText()
            reps = reps_input.text()
            sets = sets_input.text()
            if not reps.isdigit() or not sets.isdigit():
                QMessageBox.warning(dialog, 'Invalid Input', 'Please enter valid numbers for reps and sets.')
                return
            if(len(added_exercises) == 0):
                id = 0
            else:
                id = added_exercises[-1].id + 1
            exercise_obj = ExerciseData(id, exercise, int(reps), int(sets))  # Create an Exercise object
            added_exercises.append(exercise_obj)
            exercise_details = QHBoxLayout()
            exercise_label = QLabel(f"{exercise} - Reps: {reps}, Sets: {sets}")
            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(lambda: delete_exercise(exercise_details, exercise_obj))

            exercise_details.addWidget(exercise_label)
            exercise_details.addWidget(delete_button)
            exercise_details_layout.addLayout(exercise_details)

            reps_input.clear()
            sets_input.clear()

        def delete_exercise(layout, exercise_obj):
            
            for i in reversed(range(layout.count())):
                widget = layout.itemAt(i).widget()
                if widget:
                    widget.deleteLater()
            layout.setParent(None)
            layout.deleteLater()

            # Now remove the corresponding exercise object from the list
            for i, ex in enumerate(added_exercises, start = 0):
                if(exercise_obj.id == ex.id):
                    added_exercises.pop(i)
                    break
            

        add_exercise_button.clicked.connect(add_exercise_to_list)

        layout.addLayout(exercise_details_layout)
        exercise_entry_layout = QHBoxLayout()
        exercise_entry_layout.addWidget(QLabel("Exercise"))
        exercise_entry_layout.addWidget(exercise_input)
        exercise_entry_layout.addWidget(QLabel("Reps"))
        exercise_entry_layout.addWidget(reps_input)
        exercise_entry_layout.addWidget(QLabel("Sets"))
        exercise_entry_layout.addWidget(sets_input)
        exercise_entry_layout.addWidget(add_exercise_button)
        
        layout.addLayout(exercise_entry_layout)

        # Dialog buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(lambda: self.accept_dialog(dialog, title_input, duration_input, type_input, description_input, added_exercises))
        buttons.accepted.connect(lambda: self.exercise_manager.remove_exercise(scheme.id))
        buttons.accepted.connect(lambda: self.update_ui())
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        dialog.setLayout(layout)
        dialog.exec_()

    def accept_dialog(self, dialog, title_input, duration_input, type_input, description_input, added_exercises):
        # Check if all required fields are filled and at least one exercise has been added
        if (title_input.text().strip() and 
            duration_input.currentText().strip() and 
            type_input.currentText().strip() and 
            description_input.toPlainText().strip() and
            added_exercises):
            
            title = title_input.text().strip()
            duration = duration_input.currentText().strip()
            type = type_input.currentText().strip()
            description = description_input.toPlainText().strip()
            
            self.save_new_exercise_scheme(title, duration, type, description, added_exercises)
            dialog.accept()
        else:
            QMessageBox.warning(dialog, 'Invalid Input', 'Please fill all required fields and add at least one exercise.')

    def save_new_exercise_scheme(self, title, duration, type, description, exercises):
        # Save the new exercise scheme using your exercise manager class
        self.exercise_manager.add_exercise(title, duration, type, description, exercises)
        self.update_ui()  # Refresh the UI to show the new exercise


    def update_ui(self):
        # Clear existing widgets in the layout
        for i in reversed(range(self.exercise_scheme_layout.count())):
            widget_to_remove = self.exercise_scheme_layout.itemAt(i).widget()
            self.exercise_scheme_layout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)

        # Add updated list of exercises
        for scheme in self.exercise_manager.exercises:
            self.exercise_scheme_layout.addWidget(self.create_scheme_card(scheme))
    
    from PyQt5.QtWidgets import QPushButton

    def create_scheme_card(self, scheme):
        # Create a card frame
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

        # Title, duration, and type
        title_label = QLabel(f"{scheme.title}")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setStyleSheet(
            """
            QLabel {
                border: none;  /* This removes the border if any exists */
            }
            """
        )
        layout.addWidget(title_label)

        details_label = QLabel(f"Duration: {scheme.duration}, Type: {scheme.type}")
        details_label.setFont(QFont("Arial", 14))
        details_label.setStyleSheet(
            """
            QLabel {
                border: none;  /* Removes border if any */
            }
            """
        )
        layout.addWidget(details_label)

        # Description
        description_label = QLabel(f"Description: {scheme.description}")
        description_label.setFont(QFont("Arial", 12))
        description_label.setWordWrap(True)
        description_label.setStyleSheet(
            """
            QLabel {
                border: none;  /* Removes border if any */
            }
            """
        )
        layout.addWidget(description_label)

        # List of exercises
        exercises_label = QLabel("Exercises:")
        exercises_label.setFont(QFont("Arial", 14, QFont.Bold))
        exercises_label.setStyleSheet(
            """
            QLabel {
                border: none;  /* Removes border if any */
            }
            """
        )
        layout.addWidget(exercises_label)

        for ex in scheme.exercise:
            exercise_label = QLabel(f"{ex.exercise_name} - Reps: {ex.reps}, Sets: {ex.sets}")
            exercise_label.setFont(QFont("Arial", 12))
            exercise_label.setStyleSheet(
                """
                QLabel {
                    border: none;  /* Removes border if any */
                }
                """
            )
            layout.addWidget(exercise_label)

            # Add a spacer item for spacing
            spacer = QSpacerItem(0, 2, QSizePolicy.Minimum, QSizePolicy.Fixed)  # 10px vertical spacing
            layout.addItem(spacer)

        # Add Edit and Delete buttons
        button_layout = QHBoxLayout()
        edit_button = QPushButton("Edit")
        delete_button = QPushButton("Delete")

        edit_button.setFont(QFont("Inter", 12))
        delete_button.setFont(QFont("Inter", 12))

        edit_button.setStyleSheet("""
            QPushButton {
                background-color: #2E3B55;
                color: white;
                padding: 5px 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #405372;
            }
        """)

        delete_button.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                padding: 5px 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #8B0000;
            }
        """)

        # Connect buttons to their functionalities
        delete_button.clicked.connect(lambda: self.confirm_deletion(scheme))
        edit_button.clicked.connect(lambda: self.edit_exercise_scheme(scheme))

        button_layout.addWidget(edit_button)
        button_layout.addWidget(delete_button)
        layout.addLayout(button_layout)
        
        card.setLayout(layout)
        return card

    def confirm_deletion(self, scheme):
        reply = QMessageBox.question(self, 'Confirm Deletion', 'Are you sure you want to delete this scheme?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.exercise_manager.remove_exercise(scheme.id)
            self.update_ui()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Exercise()
    window.show()
    sys.exit(app.exec_())
