import sys
import os
import time

from PyQt5.QtWidgets import (
    QFrame, QApplication, QMessageBox, QGraphicsDropShadowEffect, QMainWindow,
    QTextEdit, QVBoxLayout, QSpacerItem, QSizePolicy, QHBoxLayout, QWidget,
    QPushButton, QLabel, QStackedLayout, QLineEdit, QStackedWidget,
    QScrollArea, QGridLayout,QComboBox
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QSize, QTimer, QTimer
from PyQt5.QtGui import QColor, QPalette, QIcon, QFont, QIntValidator
from winotify import Notification, audio

from backend.controllers.NotifikasiController import NotifikasiController, ListNotifikasiController



class NotifCard(QWidget):
    def __init__(self,  db_fileName , notif_data , update_ui_callback = None  ,parent = None):
        super().__init__(parent)

        self.parent_window = parent
        self._notif_data = notif_data
        self.db_fileName = db_fileName
        self.update_ui = update_ui_callback

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

        # Buttons
        button_layout = QHBoxLayout()
        edit_button = QPushButton("Edit")
        delete_button = QPushButton("Delete")

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

        delete_button.clicked.connect(self.confirm_deletion)
        edit_button.clicked.connect(self.edit_action)

        button_layout.addWidget(edit_button)
        button_layout.addWidget(delete_button)
        card_layout.addLayout(button_layout)

        card.setLayout(card_layout)

        # Add card to the main layout of NotifCard
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(card)

    def confirm_deletion(self):
        reply = QMessageBox.question(self, 'Confirm Deletion', 'Are you sure you want to delete this scheme?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            
            notif_controller = NotifikasiController(self.db_fileName)
            notif_controller.deleteNotifikasi(self._notif_data)
    
            if self.update_ui:
                self.update_ui()
    def edit_action(self):
        self.parent_window.setCurrentNotif(self._notif_data)
        self.parent_window.prepareEditPage()
        


class AddNotifPage(QWidget):
    def __init__(self, db_fileName, return_callback, update_ui_callback):
        super().__init__()
        self.db_fileName = db_fileName
        self.return_callback = return_callback
        self.update_ui = update_ui_callback

        # Layout utama
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        # Judul halaman
        title = QLabel("Add New Notification")
        title.setFont(QFont("Inter", 24, QFont.Bold))
        title.setStyleSheet("color: #2F3A59;")
        layout.addWidget(title)

        # Input nama notifikasi
        nama_layout = QHBoxLayout()
        nama_label = QLabel("Name Notification:")
        self.nama_input = QLineEdit()
        nama_layout.addWidget(nama_label)
        nama_layout.addWidget(self.nama_input)
        layout.addLayout(nama_layout)

        # Dropdown untuk tanggal
        tanggal_layout = QHBoxLayout()
        tanggal_label = QLabel("Date:")
        
        
        # Dropdown Tanggal
        self.tanggal_dropdown = QComboBox()
        self.tanggal_dropdown.addItem("Select Date")
        self.tanggal_dropdown.addItems([str(i) for i in range(1, 32)])
        
        # Dropdown Bulan
        self.bulan_dropdown = QComboBox()
        self.bulan_dropdown.addItem("Select Month")
        bulan_list = [
            "January", "February", "March", "April", 
            "May", "June", "July", "August", 
            "September", "October", "November", "December"
        ]
        self.bulan_dropdown.addItems(bulan_list)
        
        # Dropdown Tahun
        self.tahun_dropdown = QComboBox()
        self.tahun_dropdown.addItem("Select Year")
        self.tahun_dropdown.addItems([str(i) for i in range(2024, 2035)])

        tanggal_layout.addWidget(tanggal_label)
        tanggal_layout.addWidget(self.tanggal_dropdown)
        tanggal_layout.addWidget(self.bulan_dropdown)
        tanggal_layout.addWidget(self.tahun_dropdown)
        layout.addLayout(tanggal_layout)

        # Dropdown untuk waktu
        waktu_layout = QHBoxLayout()
        waktu_label = QLabel("Time:")
        
        # Dropdown Jam
        self.jam_dropdown = QComboBox()
        self.jam_dropdown.addItem("Select Hour")
        self.jam_dropdown.addItems([f"{i:02d}" for i in range(24)])
        
        # Dropdown Menit
        self.menit_dropdown = QComboBox()
        self.menit_dropdown.addItem("Select Minute")
        self.menit_dropdown.addItems([f"{i:02d}" for i in range(60)])
        
        # Dropdown Detik
        self.detik_dropdown = QComboBox()
        self.detik_dropdown.addItem("Select Second") 
        self.detik_dropdown.addItems([f"{i:02d}" for i in range(60)])

        waktu_layout.addWidget(waktu_label)
        waktu_layout.addWidget(self.jam_dropdown)
        waktu_layout.addWidget(self.menit_dropdown)
        waktu_layout.addWidget(self.detik_dropdown)
        layout.addLayout(waktu_layout)

        # Tombol Simpan dan Batal
        button_layout = QHBoxLayout()
        simpan_button = QPushButton("Save")
        batal_button = QPushButton("Cancel")

        simpan_button.setStyleSheet("""
            QPushButton {
                background-color: #2E3B55;
                color: white;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #405372;
            }
        """)

        batal_button.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #8B0000;
            }
        """)

        simpan_button.clicked.connect(self.simpan_notifikasi)
        batal_button.clicked.connect(self.return_to_main)

        button_layout.addWidget(simpan_button)
        button_layout.addWidget(batal_button)
        layout.addLayout(button_layout)

    def simpan_notifikasi(self):
        # Validasi input nama notifikasi
        nama = self.nama_input.text().strip()
        if not nama:
            QMessageBox.warning(self, "Warning", "Notification name cannot be empty!")
            return

        # Ambil data dari dropdown
        tanggal = self.tanggal_dropdown.currentText()
        bulan = self.bulan_dropdown.currentText()
        tahun = self.tahun_dropdown.currentText()
        jam = self.jam_dropdown.currentText()
        menit = self.menit_dropdown.currentText()
        detik = self.detik_dropdown.currentText()

        # Validasi dropdown
        if tanggal == "Select Date":
            QMessageBox.warning(self, "Warning", "Please select a valid date!")
            return

        if bulan == "Select Month":
            QMessageBox.warning(self, "Warning", "Please select a valid month!")
            return

        if tahun == "Select Year":
            QMessageBox.warning(self, "Warning", "Please select a valid year!")
            return

        if jam == "Select Hour":
            QMessageBox.warning(self, "Warning", "Please select a valid hour!")
            return

        if menit == "Select Minute":
            QMessageBox.warning(self, "Warning", "Please select a valid minute!")
            return

        if detik == "Select Second":
            QMessageBox.warning(self, "Warning", "Please select a valid second!")
            return
        # Format tanggal
        formatted_tanggal = f"{tanggal} {bulan} {tahun}"

        # Format jam
        formatted_jam = (int(jam),int(menit),int(detik))

        # Siapkan data notifikasi
        notif_data = {
            'nama': nama,
            'tanggal': formatted_tanggal,
            'jam': formatted_jam
        }
        
        # Simpan notifikasi
        notif_controller = NotifikasiController(self.db_fileName)
        notif_controller.createNotifikasi(notif_data)

        self.nama_input.clear()

        self.tanggal_dropdown.setCurrentIndex(0)
        self.bulan_dropdown.setCurrentIndex(0)
        self.tahun_dropdown.setCurrentIndex(0)
        self.jam_dropdown.setCurrentIndex(0)
        self.menit_dropdown.setCurrentIndex(0)
        self.detik_dropdown.setCurrentIndex(0)
        # Kembali ke halaman utama dan refresh
        self.update_ui()
        self.return_callback()


    def return_to_main(self):
        # Kembali ke halaman utama
        if self.return_callback:
            self.return_callback()

class EditNotifPage(QWidget):
    def __init__(self, data_notif,db_fileName, return_callback, update_ui_callback):
        super().__init__()
        self._data_notif = data_notif
        self.db_fileName = db_fileName
        self.return_callback = return_callback
        self.update_ui = update_ui_callback
        
        if(data_notif):

            self.curr_date,self.curr_month,self.curr_year = data_notif['tanggal'].split()

            # Layout utama
            layout = QVBoxLayout(self)
            layout.setSpacing(10)
            layout.setContentsMargins(20, 20, 20, 20)

            # Judul halaman
            title = QLabel("Edit Notification")
            title.setFont(QFont("Inter", 24, QFont.Bold))
            title.setStyleSheet("color: #2F3A59;")
            layout.addWidget(title)

            # Input nama notifikasi
            nama_layout = QHBoxLayout()
            nama_label = QLabel("Name Notification:")
            self.nama_input = QLineEdit(self._data_notif['nama'])
            nama_layout.addWidget(nama_label)
            nama_layout.addWidget(self.nama_input)
            layout.addLayout(nama_layout)

            # Dropdown untuk tanggal
            tanggal_layout = QHBoxLayout()
            tanggal_label = QLabel("Date:")
            
            
            # Dropdown Tanggal
            self.tanggal_dropdown = QComboBox()
            self.tanggal_dropdown.setCurrentText(self.curr_date)
            self.tanggal_dropdown.addItem("Select Date")
            self.tanggal_dropdown.addItems([str(i) for i in range(1, 32)])
            
            # Dropdown Bulan
            self.bulan_dropdown = QComboBox()
            self.bulan_dropdown.setCurrentText(self.curr_month)
            self.bulan_dropdown.addItem("Select Month")
            bulan_list = [
                "January", "February", "March", "April", 
                "May", "June", "July", "August", 
                "September", "October", "November", "December"
            ]
            self.bulan_dropdown.addItems(bulan_list)
            
            # Dropdown Tahun
            self.tahun_dropdown = QComboBox()
            
            self.tahun_dropdown.addItem("Select Year")
            self.tahun_dropdown.setCurrentText(self.curr_year)
            self.tahun_dropdown.addItems([str(i) for i in range(2024, 2035)])

            tanggal_layout.addWidget(tanggal_label)
            tanggal_layout.addWidget(self.tanggal_dropdown)
            tanggal_layout.addWidget(self.bulan_dropdown)
            tanggal_layout.addWidget(self.tahun_dropdown)
            layout.addLayout(tanggal_layout)

            # Dropdown untuk waktu
            waktu_layout = QHBoxLayout()
            waktu_label = QLabel("Time:")
            
            # Dropdown Jam
            self.jam_dropdown = QComboBox()
            self.jam_dropdown.setCurrentText(f"{data_notif['jam'][0]:02d}")
            self.jam_dropdown.addItem("Select Hour")
            self.jam_dropdown.addItems([f"{i:02d}" for i in range(24)])
            
            # Dropdown Menit
            self.menit_dropdown = QComboBox()
            self.menit_dropdown.setCurrentText(f"{data_notif['jam'][1]:02d}")
            self.menit_dropdown.addItem("Select Minute")
            self.menit_dropdown.addItems([f"{i:02d}" for i in range(60)])
            
            # Dropdown Detik
            self.detik_dropdown = QComboBox()
            self.detik_dropdown.setCurrentText(f"{data_notif['jam'][2]:02d}")
            self.detik_dropdown.addItem("Select Second") 
            self.detik_dropdown.addItems([f"{i:02d}" for i in range(60)])

            waktu_layout.addWidget(waktu_label)
            waktu_layout.addWidget(self.jam_dropdown)
            waktu_layout.addWidget(self.menit_dropdown)
            waktu_layout.addWidget(self.detik_dropdown)
            layout.addLayout(waktu_layout)

            # Tombol Simpan dan Batal
            button_layout = QHBoxLayout()
            simpan_button = QPushButton("Save")
            batal_button = QPushButton("Cancel")

            simpan_button.setStyleSheet("""
                QPushButton {
                    background-color: #2E3B55;
                    color: white;
                    padding: 10px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #405372;
                }
            """)

            batal_button.setStyleSheet("""
                QPushButton {
                    background-color: red;
                    color: white;
                    padding: 10px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #8B0000;
                }
            """)

            simpan_button.clicked.connect(self.simpan_notifikasi)
            batal_button.clicked.connect(self.return_to_main)

            button_layout.addWidget(simpan_button)
            button_layout.addWidget(batal_button)
            layout.addLayout(button_layout)
        else:
            print("Tidak ada data notif")

    def simpan_notifikasi(self):
        # Validasi input nama notifikasi
        nama = self.nama_input.text().strip()
        if not nama:
            QMessageBox.warning(self, "Warning", "Notification name cannot be empty!")
            return

        # Ambil data dari dropdown
        tanggal = self.tanggal_dropdown.currentText()
        bulan = self.bulan_dropdown.currentText()
        tahun = self.tahun_dropdown.currentText()
        jam = self.jam_dropdown.currentText()
        menit = self.menit_dropdown.currentText()
        detik = self.detik_dropdown.currentText()

        # Validasi dropdown
        if tanggal == "Select Date":
            QMessageBox.warning(self, "Warning", "Please select a valid date!")
            return

        if bulan == "Select Month":
            QMessageBox.warning(self, "Warning", "Please select a valid month!")
            return

        if tahun == "Select Year":
            QMessageBox.warning(self, "Warning", "Please select a valid year!")
            return

        if jam == "Select Hour":
            QMessageBox.warning(self, "Warning", "Please select a valid hour!")
            return

        if menit == "Select Minute":
            QMessageBox.warning(self, "Warning", "Please select a valid minute!")
            return

        if detik == "Select Second":
            QMessageBox.warning(self, "Warning", "Please select a valid second!")
            return
        # Format tanggal
        formatted_tanggal = f"{tanggal} {bulan} {tahun}"

        # Format jam
        formatted_jam = (int(jam),int(menit),int(detik))

        # Siapkan data notifikasi
        self._data_notif['nama'] = nama
        self._data_notif['tanggal'] = formatted_tanggal
        self._data_notif['jam'] = formatted_jam
        # Simpan notifikasi
        notif_controller = NotifikasiController(self.db_fileName)
        notif_controller.updateNotifikasi(self._data_notif)

        self.nama_input.clear()

        self.tanggal_dropdown.setCurrentIndex(0)
        self.bulan_dropdown.setCurrentIndex(0)
        self.tahun_dropdown.setCurrentIndex(0)
        self.jam_dropdown.setCurrentIndex(0)
        self.menit_dropdown.setCurrentIndex(0)
        self.detik_dropdown.setCurrentIndex(0)
        # Kembali ke halaman utama dan refresh
        self.update_ui()
        self.return_callback()

    def return_to_main(self):
        # Kembali ke halaman utama
        if self.return_callback:
            self.return_callback()

class DisplayNotif(QWidget):
    def __init__(self, db_fileName):
        super().__init__()
        self._db_fileName = db_fileName
        self._list_notif_controller = ListNotifikasiController(db_fileName)
        self._list_notif = self._list_notif_controller.getListNotifikasi()
        self._list_notif.sort(key=lambda x: x["epoch"], reverse=True)
        self._current_notif = None
        self.current_epoch_time = None
        self._queue = None
        
        
        self.stacked_widget = QStackedLayout(self)

        # Halaman utama
        main_page = QWidget()
        main_layout = QVBoxLayout(main_page)
        main_layout.setContentsMargins(10, 0, 0, 0)
        main_layout.setSpacing(0)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_time)
        self.timer.start(1000)
        

        # Header
        header = QLabel("Notifikasi")
        header.setFont(QFont("Inter", 36, QFont.Bold))
        header.setStyleSheet("color: #2F3A59; margin-left:20px;")
        header.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(header)

        # Scroll area untuk notifikasi
        scroll_area = QScrollArea()
        scroll_content = QWidget()
        self.notif_layout = QGridLayout(scroll_content)
        self.notif_layout.setSpacing(10)

        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_content)
        scroll_area.setStyleSheet("border: none;")

        main_layout.addWidget(scroll_area)

        # Menambahkan NotifCard ke dalam grid layout
        if not self._list_notif:  # Mengecek jika list kosong
            empty_label = QLabel("No notifications available.")
            empty_label.setAlignment(Qt.AlignCenter)
            self.notif_layout.addWidget(empty_label, 0, 0) 
        else:
            row = 0
            col = 0
            for notif_data in self._list_notif:
                notif_card = NotifCard(db_fileName, notif_data, update_ui_callback=self.refresh_notifikasi, parent=self)
                self.notif_layout.addWidget(notif_card, row, col)

                col += 1
                if col > 1:
                    col = 0
                    row += 1

        # Tombol tambah
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

        # Layout untuk positioning tombol tambah
        
        main_layout.addWidget(add_button, alignment=Qt.AlignRight | Qt.AlignBottom)
        main_page.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.stacked_widget.addWidget(main_page)
        self.stacked_widget.setCurrentIndex(0)

        add_page = AddNotifPage(db_fileName, 
                                return_callback=lambda: self.stacked_widget.setCurrentIndex(0),update_ui_callback=self.refresh_notifikasi)
        self.stacked_widget.addWidget(add_page)

        self.edit_page = None
        # Hubungkan tombol tambah dengan perpindahan halaman
        add_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        

    def refresh_notifikasi(self):
            # Hapus semua widget dari layout
            for i in reversed(range(self.notif_layout.count())): 
                widget = self.notif_layout.itemAt(i).widget()
                if widget is not None:
                    widget.deleteLater()

            # Ambil ulang data notifikasi
            self._list_notif = self._list_notif_controller.getListNotifikasi()
            self._list_notif.sort(key=lambda x: x["epoch"], reverse=True)
            

            # Tambahkan kembali card
            row = 0
            col = 0
            if not self._list_notif:  # Mengecek jika list kosong
                empty_label = QLabel("No notifications available.")
                empty_label.setAlignment(Qt.AlignCenter)
                self.notif_layout.addWidget(empty_label, 0, 0) 
            else:
                for notif_data in self._list_notif:
                    notif_card = NotifCard(self._db_fileName, notif_data, update_ui_callback=self.refresh_notifikasi,parent = self)
                    self.notif_layout.addWidget(notif_card, row, col)

                    col += 1
                    if col > 1: 
                        col = 0
                        row += 1
            
    def setCurrentNotif(self,notif_data):
        self._current_notif = notif_data

    def prepareEditPage(self):
        # Hapus halaman edit lama jika sudah ada
        if self.edit_page:
            self.stacked_widget.removeWidget(self.edit_page)
            self.edit_page.deleteLater()
        # Buat halaman edit baru dengan data notifikasi saat ini
        self.edit_page = EditNotifPage(
            self._current_notif, 
            self._db_fileName,
            return_callback=lambda: self.stacked_widget.setCurrentIndex(0),
            update_ui_callback=self.refresh_notifikasi
        )
        
        # Tambahkan halaman edit ke stacked widget dan pindah ke halaman edit
        self.stacked_widget.addWidget(self.edit_page)
        self.stacked_widget.setCurrentWidget(self.edit_page)

    def check_time(self):
        self.current_epoch_time = int(time.time())


        if self._list_notif:
            self._queue = [notif for notif in self._list_notif if notif['epoch'] >= self.current_epoch_time]
            
            for notif in self._queue:
                if self.current_epoch_time >= notif['epoch']:
                    self.show_notifications(notif)
                    self._queue.remove(notif)
                    self.refresh_notifikasi()

    def show_notifications(self,notif):
        notification = Notification(
            app_id = "AMBATUFIT",
            title = "It’s Activity Time!",
            msg = notif['nama'],
            duration = "long"
        )
        
        
        notification.set_audio(audio.LoopingAlarm, loop = False)
        notification.show()





