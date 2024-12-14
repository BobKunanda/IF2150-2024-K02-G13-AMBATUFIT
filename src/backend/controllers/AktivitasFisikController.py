import sys
import os
from datetime import datetime
# Pastikan kita menambahkan path ke folder src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from src.backend.models.AktivitasFisik import AktivitasFisik, ListAktivitas

class AktivitasFisikController:
    def __init__(self,db_fileName):
        self._model_aktivitas = AktivitasFisik(db_fileName)
    
    #Dari id ke isi database buat display
    def getAktivitas(self,id):
        self._model_aktivitas.setLogId(id)
        self._model_aktivitas.get_log()

        date = self._model_aktivitas.getDate()
        dt = datetime.strptime(date, "%Y-%m-%d %H:%M")

        # Format the time as "HH:MM"
        time_str = dt.strftime("%H:%M")


        data_log = {
            'id' : self._model_aktivitas.getLogId(),
            'date' : dt.date(),
            'id_aktivitas' : self._model_aktivitas.getActivityId(),
            'nama_aktivitas' : self._model_aktivitas.getActivityName(),
            'capaian': self._model_aktivitas.getAchievement(),
            'kalori' : self._model_aktivitas.getCalorie(),
            'jam': time_str
        }

        return data_log
    
    #Dari form log ke database
    def addAktivitas(self, data_log):
        _date = datetime.strptime(data_log['date'], "%Y-%m-%d").date()
        _time = datetime.strptime(data_log['jam'], "%H:%M").time()
        _datetime = datetime.combine(_date, _time)
        self._model_aktivitas.setDate(_datetime)
        self._model_aktivitas.setActivityId(data_log['id_aktivitas'])
        self._model_aktivitas.setActivityId(data_log['nama_aktivitas'])
        self._model_aktivitas.setAchivement(data_log['capaian'])
        self._model_aktivitas.setCalorie(data_log['kalori'])
        self._model_aktivitas.createAktivitas()
            
    def deleteAktivitas(self,data_log):
        self._model_aktivitas.setId(data_log['id'])
        self._model_Aktivitas.deleteAktivitas()

class ListAktivitasController:
    def __init__(self, db_filename):
        self._list_aktivitas_model = ListAktivitas(db_filename)
        self._aktivitas_controller = AktivitasFisikController(db_filename)

    def getListAktivitas(self):
        listAktivitas = []
        if self._list_aktivitas_model.getListAktivitas():
            for aktivitas in self._list_aktivitas_model.getListAktivitas():
                data = self._aktivitas_controller.getAktivitas(aktivitas[0])
                listAktivitas.append(data)
        return listAktivitas
    
    def getListAktivitasValid(self):
        aktivitas_valid = []
        result = self._list_aktivitas_model.getAktivitasValid()
        for i in result:
            aktivitas_valid.append(i[0])
        
        return aktivitas_valid
    
if __name__ == "__main__":
    list = ListAktivitasController("src/data/data.db").getListAktivitas()
    print(list)