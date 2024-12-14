from src.data.database import connect_db, execute_query, fetch_one

class AktivitasFisik:
    def __init__(self, db_filename):
        self.db_filename = db_filename
        self._log_id = None
        self._date = None
        self._activity_id = None
        self._achievement = None
        self._calorie = None

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

    # Setter methods
    def setLogId(self, log_id):
        self._log_id = log_id

    def setDate(self, date):
        self._date = date

    def setActivityId(self, activity_id):
        self._activity_id = activity_id

    def setAchhievement(self, achievement):
        self._achievement = achievement

    def setCalorie(self, calorie):
        self._calorie = calorie

    
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

