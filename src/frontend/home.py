import os
import time
from PyQt5.QtWidgets import (QMessageBox,QGraphicsDropShadowEffect, QTextEdit, QVBoxLayout,QSpacerItem, 
                             QSizePolicy, QHBoxLayout, QWidget, QPushButton, QLabel, 
                             QStackedLayout, QLineEdit, QScrollArea, QFrame)
from PyQt5.QtCore import Qt, QPropertyAnimation, QSize, QTimer
from PyQt5.QtGui import QColor, QPalette, QIcon, QFont,QIntValidator,QPixmap

from .profile import Profile
from backend.controllers.NotifikasiController import ListNotifikasiController
from backend.controllers.PersonalDataController import ProfileController


class NotifCardHome(QWidget):
    def __init__(self,notif_data):
        super().__init__()
        card = QFrame()
        self.setFixedWidth(300)
        card.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border-radius: 30px;
                border: 1px solid #DDDDDD;
            }
            """
        )
        card.setFixedHeight(200)  # Adjust height for better appearance

        # Layout untuk card
        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(10, 10, 10, 10)  # Margin dalam card
        card_layout.setSpacing(15)

        # Title, duration, and type
        title_label = QLabel(f"{notif_data['nama']}")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setStyleSheet("border:none;")
        card_layout.addWidget(title_label)

        details_label = QLabel(f"{notif_data['tanggal']}")
        details_label.setFont(QFont("Arial", 14))
        details_label.setStyleSheet("border:none;")
        card_layout.addWidget(details_label)

        # Description
        jam,menit,detik = notif_data['jam']
        description_label = QLabel(f"{jam:02d}:{menit:02d}:{detik:02d}")
        description_label.setFont(QFont("Arial", 12))
        description_label.setWordWrap(True)
        description_label.setStyleSheet("border:none;")
        card_layout.addWidget(description_label)

        card.setLayout(card_layout)
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(card)


class Home(QWidget):
    def __init__(self, db_filename):
        super().__init__()
        personal_controller = ProfileController(db_filename)
        notifikasi_controller = ListNotifikasiController(db_filename)
        list_notif = notifikasi_controller.getListNotifikasi()
        self.current_epoch_time = int(time.time())

        # Split notifications into upcoming and expired (late)
        self.upcoming_notif = [notif for notif in list_notif if (0 <= notif['epoch'] - self.current_epoch_time <= 3600 )]
        self.expired_notif = [notif for notif in list_notif if (0 <= self.current_epoch_time - notif['epoch'] <= 3600)]
        # Main layout
    
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 0, 0, 0)
        self.main_layout.setSpacing(10)

        # Header
        if personal_controller.get_profile_data()['nama']:
            self.header = QLabel(f"Welcome back, {personal_controller.get_profile_data()['nama']}!")
        else:
            self.header = QLabel(f"Welcome, Anonymous!")
        self.header.setFont(QFont("Inter", 36, QFont.Bold))
        self.header.setFixedHeight(100)
        self.header.setStyleSheet("color: #2F3A59; margin-left:0px;")
        self.main_layout.addWidget(self.header, alignment=Qt.AlignTop)
        ############ Notification Sections ############
        self.create_notification_section(self.main_layout, "Upcoming Notifications", self.upcoming_notif, "src/assets/icons/upcoming.png")
        self.create_notification_section(self.main_layout, "Late Notifications", self.expired_notif, "src/assets/icons/late.png")

        spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.main_layout.addItem(spacer)

    def create_notification_section(self, parent_layout, section_title, notif_list, icon_path):
        """
        Create a notification section (e.g., Upcoming or Late Notifications)
        """
        notif_widget = QWidget()
        notif_layout = QVBoxLayout(notif_widget)
        notif_layout.setContentsMargins(0, 0, 0, 0)
        notif_layout.setSpacing(10)

        # Section label
        section_label = QWidget()
        section_label.setFixedHeight(80)
        section_label_layout = QHBoxLayout(section_label)
        section_label_layout.setContentsMargins(0, 0, 0, 0)
        section_label_layout.setSpacing(10)

        # Title and icon
        title_label = QLabel(section_title)
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        section_label_layout.addWidget(title_label)

        section_icon = QLabel()
        pixmap = QPixmap(os.path.abspath(icon_path))
        scaled_pixmap = pixmap.scaled(40, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        section_icon.setPixmap(scaled_pixmap)
        section_label_layout.addWidget(section_icon)

        # Spacer
        spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        section_label_layout.addItem(spacer)

        notif_layout.addWidget(section_label)

        # Scroll area for notifications
        scroll_area = QScrollArea()
        scroll_content = QWidget()
        notif_cards_layout = QHBoxLayout(scroll_content)
        notif_cards_layout.setContentsMargins(0,0,0,0)
        notif_cards_layout.setSpacing(10)

        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_content)
        scroll_area.setStyleSheet("border: none;")

        notif_layout.addWidget(scroll_area)

        # Populate notifications
        if not notif_list:
            empty_label = QLabel(f"No {section_title.lower()}.")
            empty_label.setAlignment(Qt.AlignCenter)
            notif_cards_layout.addWidget(empty_label, alignment=Qt.AlignCenter)
        else:
            for notif_data in notif_list:
                notif_card = NotifCardHome(notif_data)
                notif_cards_layout.addWidget(notif_card,alignment=Qt.AlignLeft)
            spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
            notif_cards_layout.addItem(spacer)

        # Add to parent layout
        parent_layout.addWidget(notif_widget, alignment=Qt.AlignTop)

    def refresh_name(self, name):
        self.header.setText(f"Welcome back, {name}!")
    def refresh_notif(self,upcoming_list,late_list):
        widget = self.main_layout.itemAt(1).widget()
        if widget is not None:
            widget.deleteLater()
        widget = self.main_layout.itemAt(2).widget()
        if widget is not None:
            widget.deleteLater()

        self.create_notification_section(self.main_layout, "Upcoming Notifications", upcoming_list, "src/assets/icons/upcoming.png")
        self.create_notification_section(self.main_layout, "Late Notifications", late_list, "src/assets/icons/late.png")

        



