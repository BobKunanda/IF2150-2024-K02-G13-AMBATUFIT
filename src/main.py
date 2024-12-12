import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel,QStackedLayout
from frontend.sidebar import SideBar
from frontend.profile import Profile
from PyQt5.QtGui import QFontDatabase, QFont, QIcon
from frontend.Exercise.exercise import Exercise
font_path = "src/assets/fonts/pjs-med.ttf"
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ambatufit")
        self.setWindowIcon(QIcon("src/assets/icons/logo.jpg"))
        self.mainLayout = QHBoxLayout()
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.mainLayout.setSpacing(0)

        self.pageManager = QStackedLayout()
        self.subContainer = QWidget()
        self.sidebar = SideBar()

        self.mainLayout.addWidget(self.sidebar)

        # Ini bakalan diisi ntar
        db_filename = os.path.join(os.path.dirname(__file__), 'data', 'data.db')
        profile = Profile(db_filename)
        self.pageManager.addWidget(profile)

        home = QLabel("Home")
        self.pageManager.addWidget(home)
        self.pageManager.setCurrentWidget(home) # --> Defaulnya bakal nampilin home dulu
        
        excercise = Exercise()
        self.pageManager.addWidget(excercise)

        activity = QLabel("activity")
        self.pageManager.addWidget(activity)

        nutrition = QLabel("nutrition")
        self.pageManager.addWidget(nutrition)

        advice = QLabel("advice")
        self.pageManager.addWidget(advice)

        notification = QLabel("notification")
        self.pageManager.addWidget(notification)
        #----------------------------------------------------------#

        self.subContainer.setLayout(self.pageManager)

        self.mainLayout.addWidget(self.subContainer)

        main_widget = QWidget()
        main_widget.setLayout(self.mainLayout)
        self.setCentralWidget(main_widget)

        self.setWindowTitle("Main")
        self.setGeometry(100, 100, 800, 600)

        # Pilihan tombol
        self.sidebar.profileButton.clicked.connect(lambda:self.displayProfile(profile))
        self.sidebar.button_widgets[0].clicked.connect(lambda: self.displayHome(home))
        self.sidebar.button_widgets[1].clicked.connect(lambda: self.displayExercise(excercise))
        self.sidebar.button_widgets[2].clicked.connect(lambda: self.displayActivity(activity))
        self.sidebar.button_widgets[3].clicked.connect(lambda: self.displayNutrion(nutrition))
        self.sidebar.button_widgets[4].clicked.connect(lambda: self.displayAdvice(advice))
        self.sidebar.button_widgets[5].clicked.connect(lambda: self.displayNotification(notification))    
        
        # Font
        self.font_id = QFontDatabase.addApplicationFont(font_path)
        self.font_family = QFontDatabase.applicationFontFamilies(self.font_id)[0]

    def displayProfile(self,widget):
        self.pageManager.setCurrentWidget(widget)

    def displayHome(self, widget):
        self.pageManager.setCurrentWidget(widget)

    def displayExercise(self, widget):
        self.pageManager.setCurrentWidget(widget)

    def displayActivity(self, widget):
        self.pageManager.setCurrentWidget(widget)

    def displayNutrion(self, widget):
        self.pageManager.setCurrentWidget(widget)
    
    def displayAdvice(self, widget):
        self.pageManager.setCurrentWidget(widget)

    def displayNotification(self, widget):
        self.pageManager.setCurrentWidget(widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    custom_font = QFont(window.font_family, 10)
    app.setFont(custom_font)
    sys.exit(app.exec_())