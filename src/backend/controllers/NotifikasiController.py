import sys
import os
import time
from datetime import datetime
from typing import Tuple

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from src.backend.models.Notifikasi import Notifikasi, ListNotifikasi

class NotifikasiController:
    def __init__(self,db_fileName):
        self._model_notifikasi = Notifikasi(db_fileName)
    
    def getNotifikasi(self,id):
        self._model_notifikasi.setId(id)
        self._model_notifikasi.getNotifikasi()

        tanggal,jam = self.convert_epoch(self._model_notifikasi.getWaktu())


        data_notif = {
            'id' : self._model_notifikasi.getId(),
            'nama' : self._model_notifikasi.getNama(),
            'epoch' : self._model_notifikasi.getWaktu(),
            'tanggal':tanggal,
            'jam': jam
        }

        return data_notif

    def createNotifikasi(self, data_notif):
        self._model_notifikasi.setNama(data_notif['nama'])
        epoch = self.convert_to_epoch(data_notif['tanggal'],data_notif['jam'])
        self._model_notifikasi.setWaktu(epoch)
        self._model_notifikasi.createNotifikasi()
        
    def updateNotifikasi(self,data_notif):
        self._model_notifikasi.setId(data_notif['id'])
        self._model_notifikasi.setNama(data_notif['nama'])
        epoch = self.convert_to_epoch(data_notif['tanggal'],data_notif['jam'])
        self._model_notifikasi.setWaktu(epoch)
        self._model_notifikasi.updateNotifikasi()
    
    def deleteNotifikasi(self,data_notif):
        self._model_notifikasi.setId(data_notif['id'])
        self._model_notifikasi.deleteNotifikasi()

    def convert_epoch(self,epoch_time):
        # Konversi epoch ke objek datetime
        dt_object = datetime.fromtimestamp(epoch_time)

        # Format tanggal menjadi string
        date_string = dt_object.strftime("%d %B %Y")

        # Ekstrak jam, menit, dan detik
        time_tuple = (dt_object.hour, dt_object.minute, dt_object.second)

        return date_string, time_tuple
    
    def convert_to_epoch(self,date_string: str, time_tuple: Tuple[int, int, int]) -> int:
        
        dt_object = datetime.strptime(date_string, "%d %B %Y")

        
        dt_object = dt_object.replace(hour=time_tuple[0], minute=time_tuple[1], second=time_tuple[2])

       
        epoch_time = int(dt_object.timestamp())

        return epoch_time



class ListNotifikasiController:
    def __init__(self, db_filename):
        self._list_notif_model = ListNotifikasi(db_filename)
        self._notifikasi_controller = NotifikasiController(db_filename)

    def getListNotifikasi(self):
        listNotifikasi = []
        if self._list_notif_model.getListNotifikasi():
            for notifikasi in self._list_notif_model.getListNotifikasi():
                data = self._notifikasi_controller.getNotifikasi(notifikasi[0])
                listNotifikasi.append(data)
        return listNotifikasi
    
# list = ListNotifikasiController("src/data/data.db")
# print(list.getListNotifikasi())
# control = NotifikasiController("src/data/data.db")
# print(control.convert_to_epoch("14 December 2024",(2,2,3)))


        