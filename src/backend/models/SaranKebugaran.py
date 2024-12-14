import sqlite3
from src.data.database import connect_db, fetch_all, fetch_one

class SaranKebugaran:
    def __init__(self, db_filename):
        self.db_filename = db_filename
        self._data = self._load_all_saran_kebugaran()

    def _load_all_saran_kebugaran(self):
        connection, cursor = connect_db(self.db_filename)
        query = "SELECT * FROM saran_kebugaran"
        rows = fetch_all(connection, cursor, query)
        return [{"id": row[0], "saran_latihan": row[1], "saran_nutrisi": row[2]} for row in rows]
    
    def load_saran_kebugaran(self, saran_kebugaran_id):
        connection, cursor = connect_db(self.db_filename)
        query = "SELECT * FROM saran_kebugaran WHERE id = ?"
        row = fetch_one(connection, cursor, query, (saran_kebugaran_id,))
        if row:
            return {"id": row[0], "saran_latihan": row[1], "saran_nutrisi": row[2]}
        return None
