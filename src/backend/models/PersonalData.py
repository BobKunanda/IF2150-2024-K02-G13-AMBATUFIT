from src.data.database import connect_db, execute_query, fetch_one


class PersonalData:
    def __init__(self, db_filename):
        self.db_filename = db_filename
        self._nama = None
        self._usia = None
        self._tinggi = None
        self._beratBadan = None
        self._tujuanKebugaran = None
        self.get_profile()

    def getNama(self):
        return self._nama

    def getUsia(self):
        return self._usia

    def getTinggi(self):
        return self._tinggi
    
    def getBerat(self):
        return self._beratBadan

    def getTujuan(self):
        return self._tujuanKebugaran

    # Setter methods
    def setNama(self, nama):
        self._nama = nama

    def setUsia(self, usia):
        self._usia = usia

    def setTinggi(self, tinggi_badan):
        self._tinggi = tinggi_badan

    def setBerat(self, berat):
        self._beratBadan = berat

    def setTujuan(self, tujuan):
        self._tujuanKebugaran = tujuan

    # Fungsi untuk mengupdate data pada baris dengan id = 1
    def update_profile(self):
        connection, cursor = connect_db(self.db_filename)
        # Query untuk mengupdate data pada id = 1
        query = """
            UPDATE personal_data
            SET nama = ?, usia = ?, tinggi = ?, berat = ?, tujuan = ?
            WHERE id = 1
        """
        params = (self._nama, self._usia, self._tinggi, self._beratBadan, self._tujuanKebugaran)

        # Menjalankan query untuk memperbarui data
        execute_query(connection, cursor, query, params)

        # Menutup koneksi
        connection.close()

    # Fungsi untuk mendapatkan data profil (misalnya jika ingin mendapatkan data id=1)
    def get_profile(self):
        connection, cursor = connect_db(self.db_filename)

        # Query untuk mengambil data dari id = 1
        query = "SELECT * FROM personal_data WHERE id = 1"

        # Mengambil hasil data
        result = fetch_one(connection, cursor, query)

        if result:
            self._nama = result[4]
            self._usia = result[1]
            self._tinggi = result[2]
            self._beratBadan = result[5]
            self._tujuanKebugaran = result[3]

        # Menutup koneksi
        connection.close()
