import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from src.data.database import connect_db, execute_query, fetch_one, fetch_all

class AktivitasFisik:
    def __init__(self, db_filename):
        self.db_filename = db_filename
        self._log_id = None
        self._date = None
        self._activity_id = None
        self._achievement = None
        self._calorie = None
        self._activity_name = None

    def getLogId(self):
        return self._log_id

    def getDate(self):
        return self._date

    def getActivityId(self):
        return self._activity_id
    
    def getAchievement(self):
        return self._achievement

    def getCalorie(self):
        return self._calorie

    def getActivityName(self):
        return self._activity_name
    
    # Setter methods
    def setLogId(self, log_id):
        self._log_id = log_id

    def setDate(self, date):
        self._date = date

    def setActivityId(self, activity_id):
        self._activity_id = activity_id

    def setAchievement(self, achievement):
        self._achievement = achievement

    def setCalorie(self, calorie):
        self._calorie = calorie

    def setActivityName(self, activity_name):
        self._activity_ = activity_name
    
    def add_log(self):
        connection, cursor = connect_db(self.db_filename)
        # Query untuk mengupdate data pada id = 1
        query = """
            INSERT INTO aktivitas_fisik(tanggal, id_latihan, capaian, kalori)
            VALUES (?,?,?,?)
        """
        params = (self._date, self._activity_id, self._achievement, self._calorie)

        # Menjalankan query untuk memperbarui data
        execute_query(connection, cursor, query, params)

        # Menutup koneksi
        connection.close()
    
    def delete_log(self):
        connection, cursor = connect_db(self.db_filename)
        query = """
            DELETE FROM aktivitas_fisik WHERE (id_aktivitas = ?)
        """
        params = (self._log_id,)

        # Menjalankan query untuk memperbarui data
        execute_query(connection, cursor, query, params)

        # Menutup koneksi
        connection.close()

    def get_log(self):
        connection, cursor = connect_db(self.db_filename)
        query = """
            select id_aktivitas, tanggal, id_latihan, capaian, kalori, nama from aktivitas_fisik join latihan on latihan.id = aktivitas_fisik.id_latihan
            where id_aktivitas = ?
        """
        params = (self._log_id,)

        # Menjalankan query untuk memperbarui data
        result = fetch_one(connection, cursor, query, params)

        if result:
            self._log_id = result[0]
            self._date = result[1]
            self._activity_id = result[2]
            self._achievement = result[3]
            self._calorie = result[4]
            self._activity_name = result[5]

        # Menutup koneksi
        connection.close()

class ListAktivitas:
    def __init__(self, db_filename):
        self._db_filename = db_filename
        self._list_aktivitas = None

    def getListAktivitas(self):
        connection, cursor = connect_db(self._db_filename)

        query = """
            select id_aktivitas, tanggal, id_latihan, capaian, kalori, nama from aktivitas_fisik join latihan on latihan.id = aktivitas_fisik.id_latihan 
            ORDER BY id_aktivitas DESC;
        """
        
        result = fetch_all(connection,cursor,query)

        if result:
            self._list_aktivitas = result
        else:
            self._list_aktivitas = None

        connection.close()

        return self._list_aktivitas
    
    def getAktivitasValid(self):
        connection, cursor = connect_db(self._db_filename)

        query = """
            SELECT nama FROM latihan ORDER BY id;
        """
        
        result = fetch_all(connection,cursor,query)

        if result:
            self._list_aktivitas_valid = result
        else:
            self._list_aktivitas = None

        connection.close()

        return self._list_aktivitas_valid
    

if __name__ == "__main__":
    list_aktivitas = ListAktivitas("src/data/data.db")
    print(list_aktivitas.getListAktivitas())