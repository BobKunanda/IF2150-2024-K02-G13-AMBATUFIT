from src.data.database import connect_db, execute_query, fetch_one

class AktivitasFisik:
    def __init__(self, db_filename):
        self.db_filename = db_filename
        self._log_id = None
        self._date = None
        self._activity_id = None
        self._achievement = None
        self._calorie = None
        #self.get_profile()

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

    # Fungsi untuk mengupdate data pada baris dengan id = 1
    def update_log(self):
        pass

    # Fungsi untuk mendapatkan data profil (misalnya jika ingin mendapatkan data id=1)
    def add_log(self):
        pass
