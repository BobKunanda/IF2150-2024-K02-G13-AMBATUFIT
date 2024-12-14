import sys
import os
from datetime import datetime, time
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
        _date = data_log["date"].toString("yyyy-MM-dd")
        _time_hour = data_log["jam"].hour()
        _time_minute = data_log["jam"].minute()
        time_obj = time(_time_hour, _time_minute)
        formatted_time = time_obj.strftime("%H:%M")
        _datetime = _date + " " + formatted_time 
        self._model_aktivitas.setDate(_datetime)
        self._model_aktivitas.setActivityName(data_log['nama_aktivitas'])
        self._model_aktivitas.get_id_from_activity()
        self._model_aktivitas.setAchievement(data_log['capaian'])
        self._model_aktivitas.setCalorie(data_log['kalori'])
        self._model_aktivitas.add_log()
            
    def deleteAktivitas(self,data_log):

        self._model_aktivitas.setLogId(data_log['id'])
        self._model_aktivitas.delete_log()

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