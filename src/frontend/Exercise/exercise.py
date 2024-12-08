import sys
from PyQt5.QtWidgets import (
    QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox,
    QLabel, QWidget, QFrame, QScrollArea, QStackedLayout, QLineEdit, QTextEdit, QComboBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon


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
        self.exercise_layout = QVBoxLayout()
        exercise_container.setLayout(self.exercise_layout)
        scroll_area.setWidget(exercise_container)
        scroll_area.setStyleSheet("border: none;")
        layout.addWidget(scroll_area)

        # Add Default "Back Day" Card
        self.add_exercise_card("Back Day", "Duration: 30 min    Type: Strength Training", "Description", [("Push-ups", 15), ("Pull-ups", 10), ("Sit-ups", 10), ("Looks-Maxxing", 10) , ("Mewing", 25)])

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
        add_button.clicked.connect(self.add_new_exercise)
        layout.addWidget(add_button, alignment=Qt.AlignRight | Qt.AlignBottom)

        widget.setLayout(layout)
        return widget

    def content_exercise_card(self, title, info, description, list_of_exercise):
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

        # Scrollable Exercise List
        scroll_area = QScrollArea()
        scroll_area.setStyleSheet("border: none;")
        scroll_area.setWidgetResizable(True)

        exercise_list_container = QWidget()
        self.exercise_list_layout = QVBoxLayout()
        exercise_list_container.setLayout(self.exercise_list_layout)
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
        for i in reversed(range(self.exercise_list_layout.count())):
            self.exercise_list_layout.itemAt(i).widget().deleteLater()

        for exercise, reps in exercises:
            exercise_label = QLabel(f"{exercise} : {reps} reps")
            exercise_label.setFont(QFont("Inter", 14))
            exercise_label.setStyleSheet("color: #555555; border: none;")
            self.exercise_list_layout.addWidget(exercise_label)

    def add_exercise_card(self, title, info, description, exercises):
        """Adds a new exercise card to the scrollable layout."""
        card_data = (title, info, description, exercises)
        self.exercise_data.append((card_data))

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
                padding: 5px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #8B0000;
            }
            """
        )
        delete_button.setFixedWidth(150)
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
        self.exercise_layout.addWidget(card)
    
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
        layout.addWidget(self.edit_description)

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
        save_button.clicked.connect(self.save_exercise_details)
        save_button.clicked.connect(lambda: self.content_stack.setCurrentIndex(1))
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

    def save_exercise_details(self):
        """Saves the edited details back to the exercise and switches to the info card."""
        new_title = self.edit_title.text()
        new_duration = self.edit_duration.currentText()
        new_type = self.edit_type.currentText()
        new_info = f"Duration: {new_duration}    Type: {new_type}"
        new_description = self.edit_description.toPlainText()

        self.card_title.setText(new_title)
        self.card_info.setText(new_info)
        self.card_description.setText(new_description)
        
    def show_exercise_details(self, title, info, description, exercises):
        """Shows the details of a specific exercise card."""
        self.update_content_card(title, info, description, exercises)
        self.content_stack.setCurrentIndex(1)

    def add_new_exercise(self):
        """Adds a dynamically created exercise card."""
        count = self.exercise_layout.count() + 1
        self.add_exercise_card(f"Exercise {count}", "Duration: -    Type: -", "-", [("-", 0)])

    def confirm_deletion(self, card, card_data):
        reply = QMessageBox.question(self, 'Confirm Deletion', 'Are you sure you want to delete this training?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.exercise_layout.removeWidget(card)
            card.deleteLater()
            if card_data in self.exercise_data:
                self.exercise_data.remove(card_data)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Exercise()
    window.show()
    sys.exit(app.exec_())
