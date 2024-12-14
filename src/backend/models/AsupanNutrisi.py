import sqlite3
from datetime import date, datetime as dt
from types import prepare_class
from src.data.database import connect_db, execute_query, fetch_one, fetch_all

class AsupanNutrisi:
    def __init__(self, db_filename):
        self.db_filename = db_filename
        self._id = None
        self._nama = None
        self._datetime = None
        self._nutrisi = {}

    # Getters
    def get_id(self): return self._id
    def get_nama(self): return self._nama
    def get_datetime(self): return self._datetime
    def get_nutrisi(self): return self._nutrisi

    # Setters
    def set_id(self, id): self._id = id
    def set_nama(self, nama): self._nama = nama
    def set_datetime(self, datetime): self._datetime = datetime
    def set_nutrisi(self, nutrisi): self._nutrisi = nutrisi

    # Methods ke Database
    def get_all_asupan(self):
        try:
            connection, cursor = connect_db(self.db_filename)
            query_asupan = "SELECT * FROM asupan_nutrisi"
            result_asupan = fetch_all(connection, cursor, query_asupan)
            connection.close()

            # Sekarang buat ngambil kalori, protein, karbohidrat, lemak
            processed_results = []
            for row in result_asupan:
                asupan_id = row[0]
                name = row[1]
                datetime = dt.strptime(row[2], "%Y/%m/%d %H:%M")

                query_detail = """
                    SELECT id_nutrisi, kandungan
                    FROM detail_asupan_nutrisi WHERE id_asupan = ?
                """
                connection, cursor = connect_db(self.db_filename)
                result_detail = fetch_all(connection, cursor, query_detail, (row[0],))
                connection.close()

                carbs_val = 0.0
                protein_val = 0.0
                fat_val = 0.0
                mineral_val = 0.0
                air_val = 0.0

                for detail in result_detail:
                    nutrient_id = detail[0]
                    value = detail[1]
                    
                    if nutrient_id == 1:
                        carbs_val = value
                    elif nutrient_id == 2:
                        protein_val = value
                    elif nutrient_id == 3:
                        fat_val = value
                    elif nutrient_id == 4:
                        mineral_val = value
                    elif nutrient_id == 5:
                        air_val = value
                processed_results.append((asupan_id, name, datetime, carbs_val, protein_val, fat_val, mineral_val, air_val))
            processed_results = processed_results[::-1]
        except sqlite3.Error as e:
            print(f"Error fetching asupan_nutrisi data: {e}")
            raise
        return processed_results

    def load_asupan_nutrisi(self, id):
        try:
            connection, cursor = connect_db(self.db_filename)
            query_asupan = "SELECT * FROM asupan_nutrisi WHERE id = ?"
            result_asupan = fetch_one(connection, cursor, query_asupan, (id,))
            if result_asupan:
                self._id = result_asupan[0]
                self._nama = result_asupan[1]
                self._datetime = dt.strptime(result_asupan[2], "%Y/%m/%d %H:%M")
                query_detail = """
                    SELECT id_nutrisi, kandungan
                    FROM detail_asupan_nutrisi WHERE id_asupan = ?
                """
                result_detail = fetch_all(connection, cursor, query_detail, (id,))
                self._nutrisi = {row[0]: row[1] for row in result_detail}
            connection.close()
        except sqlite3.Error as e:
            print(f"Error fetching asupan_nutrisi data: {e}")
            raise
        return self

    def add_asupan_nutrisi(self, nama, datetime, nutrisi):
        try:
            connection, cursor = connect_db(self.db_filename)
            asupan_id = self.insert_asupan(connection, cursor, nama, datetime)
            self.insert_details(connection, cursor, asupan_id, nutrisi)
            connection.commit()
            connection.close()
        except sqlite3.Error as e:
            print(f"Error menambahkan data asupan_nutrisi: {e}")
            raise
    
    def insert_asupan(self, connection, cursor, nama, datetime):
        query_asupan = "INSERT INTO asupan_nutrisi (name, datetime) VALUES (?, ?)"
        execute_query(connection, cursor, query_asupan, (nama, datetime))
        return cursor.lastrowid
    
    def insert_details(self, connection, cursor, asupan_id, nutrisi):
        query_detail = """
            INSERT INTO detail_asupan_nutrisi (id_asupan, id_nutrisi, kandungan)
            VALUES (?, ?, ?)
        """
        for id_nutrisi, kandungan in nutrisi.items():
            execute_query(connection, cursor, query_detail, (asupan_id, id_nutrisi, kandungan))
    
    def update_asupan_nutrisi(self):
        try:
            connection, cursor = connect_db(self.db_filename)

            query_asupan = "UPDATE asupan_nutrisi SET name = ?, datetime = ? WHERE id = ?"
            execute_query(connection, cursor, query_asupan, (self._nama, self._datetime, self._id))

            query_delete_details = "DELETE FROM detail_asupan_nutrisi WHERE id_asupan = ?"
            execute_query(connection, cursor, query_delete_details, (self._id,))

            for id_nutrisi, kandungan in self._nutrisi.items():
                query_detail = """
                    INSERT INTO detail_asupan_nutrisi (id_asupan, id_nutrisi, kandungan)
                    VALUES (?, ?, ?)
                """
                execute_query(connection, cursor, query_detail, (self._id, id_nutrisi, kandungan))

            connection.commit()
            connection.close()

        except Exception as e:
            print(f"Error memperbarui data asupan_nutrisi: {e}")

    def delete_asupan_nutrisi(self):
        try:
            connection, cursor = connect_db(self.db_filename)
            query_delete_details = "DELETE FROM detail_asupan_nutrisi WHERE id_asupan = ?"
            execute_query(connection, cursor, query_delete_details, (self._id,))

            query_delete_asupan = "DELETE FROM asupan_nutrisi WHERE id = ?"
            execute_query(connection, cursor, query_delete_asupan, (self._id,))

            connection.commit()
            connection.close()
        except Exception as e:
            print(f"Error menghapus data asupan_nutrisi: {e}")
            raise