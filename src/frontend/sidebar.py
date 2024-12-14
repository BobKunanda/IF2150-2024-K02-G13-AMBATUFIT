import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel
from PyQt5.QtCore import Qt, QPropertyAnimation, QSize, QTimer
from PyQt5.QtGui import QColor, QPalette, QIcon, QFont, QFontDatabase, QFont

from backend.controllers.PersonalDataController import ProfileController

font_path = "src/assets/fonts/pjs-med.ttf"

class HoverButton(QPushButton):
    def __init__(self, label="", parent=None):
        super().__init__(label, parent)
        self.hover_timer = QTimer()
        self.hover_timer.setSingleShot(True)
        self.hover_timer.timeout.connect(self.apply_hover_style)
        self.default_style = """
        QPushButton {
            border: none;
            color: white;
            text-align: left;
            padding-left: 10px;
        }
        QPushButton::icon {
            padding-left: 0px; 
        }
        QPushButton:pressed {
            background-color: #1c6692;
        }
        """
        self.hover_style = """
        QPushButton {
            border: none;
            color: white;
            text-align: left;
            padding-left: 10px;
            background-color: #3498db;
            border-radius: 15px;
        }
        """
        self.active_style = """
        QPushButton {
            border: none;
            color: white;
            text-align: left;
            padding-left: 10px;
            background-color: #3498db;
            border-radius: 15px; 
        }
        """
        self.setStyleSheet(self.default_style)
        self.is_active = False

    def enterEvent(self, a0):
        if not self.is_active:
            self.hover_timer.start(100)
        super().enterEvent(a0)


    def leaveEvent(self, a0):
        if not self.is_active:
            self.hover_timer.stop()
            self.setStyleSheet(self.default_style)
        super().leaveEvent(a0)

    def apply_hover_style(self):
        if not self.is_active:
            self.setStyleSheet(self.hover_style)

    def set_active(self, active):
        self.is_active = active
        self.setStyleSheet(self.active_style if active else self.default_style)


class SideBar(QWidget):
    def __init__(self,db_filename):
        super().__init__()

        name_controller = ProfileController(db_filename)
        self._data = name_controller.get_profile_data()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
    

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(53, 62, 92))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Font
        font_path = "src/assets/fonts/pjs-med.ttf"
        self.font_id = QFontDatabase.addApplicationFont(font_path)
        self.font_family = QFontDatabase.applicationFontFamilies(self.font_id)[0]
        font = QFont(self.font_family, 9)

        self.toggleButton = QPushButton("")
        toggleIcon = QIcon(os.path.abspath("src/assets/icons/sidebar.png"))
        self.toggleButton.setIcon(toggleIcon)
        self.toggleButton.setIconSize(QSize(30, 30))
        self.toggleButton.setFixedSize(40, 40)
        self.toggleButton.setFont(font)
        self.toggleButton.setStyleSheet("""
        QPushButton {
            border: none;
        }
        QPushButton:hover {
            background-color: #000000;
        }
        """)
        layout.addWidget(self.toggleButton)


        # Setting general
        maxContainerWidth = 200

        # -------Tombol Profil--------------
        self.profileContainer = QWidget()
        profileLayout = QVBoxLayout()
        profileLayout.setContentsMargins(0, 0, 0, 0)
        profileLayout.setContentsMargins(5, 5, 0, 0) 
        profileLayout.setSpacing(0) 
        
        self.profileButton = QPushButton()
        profileIcon = QIcon(os.path.abspath("src/assets/icons/profile.png"))
        self.profileButton.setIcon(profileIcon)
        self.profileButton.setIconSize(QSize(30, 30))
        self.profileButton.setFixedSize(30, 30)
        self.profileButton.setStyleSheet("""
        QPushButton {
            border-radius: 15px;
            background-color: #ffffff;
            color: white;
            border: 2px solid #2980b9;
        }
        QPushButton:hover {
            background-color: #d3d3d3; 
        }

        """)
        profileLayout.addWidget(self.profileButton, alignment= Qt.AlignmentFlag.AlignCenter)

        name = "-"
        if self._data['nama']:
            name = self._data['nama']

        self.usernameLabel = QLabel(f"Username: {name} ")
        self.usernameLabel.setFont(font)
        self.usernameLabel.setStyleSheet("color:#ffffff")
        self.usernameLabel.hide()
        profileLayout.addWidget(self.usernameLabel, alignment=Qt.AlignmentFlag.AlignCenter)

        self.profileContainer.setLayout(profileLayout)
        self.profileContainer.setMaximumHeight(70)
        self.profileContainer.setMaximumWidth(maxContainerWidth)
        layout.addWidget(self.profileContainer)

        # List tombol dan label
        self.buttons = [
            ("src/assets/icons/home.png", "   Beranda"),
            ("src/assets/icons/exercise.png", "   Exercise"),
            ("src/assets/icons/physical.png", "   Physical Activity"),
            ("src/assets/icons/nutrition.png", "   Nutritional Intake"),
            ("src/assets/icons/advice.png", "   Fitness Advice"),
            ("src/assets/icons/notification.png", "   Notifications"),
        ]

        self.button_widgets = []
        self.button_texts = []

        for icon_path, label_text in self.buttons:
            button = HoverButton(label_text)
            button_icon = QIcon(os.path.abspath(icon_path))
            button.setIcon(button_icon)
            button.setIconSize(QSize(20, 20))
            button.setFixedSize(maxContainerWidth, 40)
            button.setFont(font)
            button.clicked.connect(lambda _, b=button: self.set_active_button(b))
            self.button_widgets.append(button)
            self.button_texts.append(label_text)
            layout.addWidget(button)

        self.toggleButton.clicked.connect(self.toggle_sidebar)

        self.setLayout(layout)

        self.collapsed_width = 40
        self.expanded_width = 200

        self.setFixedWidth(self.collapsed_width)
        self.animation = QPropertyAnimation(self, b"minimumWidth")
        self.setSizePolicy(self.sizePolicy().Expanding, self.sizePolicy().Expanding)

        self.profileButton.clicked.connect(lambda:self.set_active_button(self.profileButton))

    def toggle_sidebar(self):
        if self.width() == self.collapsed_width:
            self.animate_width(self.expanded_width)
            self.usernameLabel.show()
            for i, button in enumerate(self.button_widgets):
                button.setText(self.button_texts[i])
        else:
            self.animate_width(self.collapsed_width)
            self.usernameLabel.hide()
            for button in self.button_widgets:
                button.setText("")

    def animate_width(self, target_width):
        self.animation.setDuration(300)
        self.animation.setStartValue(self.width())
        self.animation.setEndValue(target_width)
        self.animation.start()

    def set_active_button(self, button):
        if button == self.profileButton:
            # Jika tombol profil ditekan, biarkan tetap aktif
            for btn in self.button_widgets:
                if btn != self.profileButton:
                    btn.set_active(False)
        else:
            # Tombol lainnya tidak aktif
            for btn in self.button_widgets:
                btn.set_active(False)
            button.set_active(True)

    def refresh_name(self,name):
        self.usernameLabel.setText(f"Username: {name} ")



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()
        self.sidebar = SideBar()

        layout.addWidget(self.sidebar)

        label = QLabel("Main")
        layout.addWidget(label)

        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        self.setWindowTitle("Main")
        self.setGeometry(100, 100, 800, 600)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
