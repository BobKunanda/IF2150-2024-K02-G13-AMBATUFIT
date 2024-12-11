from src.data.database import connect_db, execute_query, fetch_one

class FitnessAdvice:
    def __init__(self, db_filename):
        self.db_filename = db_filename
        self.id = None
        self.saran_latihan = None
        self.saran_nutrisi = None
        self.get_advice()

    # Getter
    def get_id(self):
        return self.id
    def get_saran_latihan(self):
        return self.saran_latihan
    def get_saran_nutrisi(self):
        return self.saran_nutrisi
        
    # Setter
    def set_id(self, id: int):
        self.id = id
    def set_saran_latihan(self, saran_latihan: str):
        self.saran_latihan = saran_latihan
    def set_saran_nutrisi(self, saran_nutrisi: str):
        self.saran_nutrisi = saran_nutrisi

        # Fetcher (dari tabel di data.db)
    def get_advice(self, id=1):
        connection, cursor = connect_db(self.db_filename)

        query = "SELECT * FROM saran_kebugaran WHERE id = ?"
        params = (id,)

        # Fetch datanya coy
        result = fetch_one(connection, cursor, query, params)

        if result:
            self.id = result[0]
            self.saran_latihan = result[1]
            self.saran_nutrisi = result[2]

        connection.close()

    def update_advice(self):
        if self.id is None:
            raise ValueError("ID must be set before updating advice.")

        connection, cursor = connect_db(self.db_filename)

        query = """
            UPDATE saran_kebugaran
            SET saran_latihan = ?, saran_nutrisi = ?
            WHERE id = ?
        """
        params = (self.saran_latihan, self.saran_nutrisi, self.id)

        # Update coy
        execute_query(connection, cursor, query, params)

        connection.close()