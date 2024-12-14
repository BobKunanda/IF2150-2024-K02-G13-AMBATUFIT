import sys
import os
from datetime import datetime as dt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from src.backend.models.AsupanNutrisi import AsupanNutrisi

class AsupanNutrisiController:
    def __init__(self, db_filename):
        self.asupan_nutrisi_model = AsupanNutrisi(db_filename)

    def get_all_asupan(self):
        try:
            return self.asupan_nutrisi_model.get_all_asupan()
        except Exception as e:
            print(f"Error fetching asupan nutrisi data: {e}")
            return []

    def load_asupan_nutrisi(self, id):
        try:
            return self.asupan_nutrisi_model.load_asupan_nutrisi(id)
        except Exception as e:
            print(f"Error loading asupan nutrisi by ID {id}: {e}")
            return None

    def add_asupan_nutrisi(self, nama, datetime, nutrisi):
        try:
            self.asupan_nutrisi_model.add_asupan_nutrisi(nama, datetime, nutrisi)
            return True
        except Exception as e:
            print(f"Error adding asupan nutrisi: {e}")
            return False

    def update_asupan_nutrisi(self, id, nama, nutrisi):
        try:
            asupan = self.asupan_nutrisi_model.load_asupan_nutrisi(id)
            if asupan:
                asupan.set_nama(nama)
                asupan.set_nutrisi(nutrisi)
                asupan.update_asupan_nutrisi()
                return True
            return False
        except Exception as e:
            print(f"Error updating asupan nutrisi: {e}")
            return False

    def delete_asupan_nutrisi(self, id):
        try:
            asupan = self.asupan_nutrisi_model.load_asupan_nutrisi(id)
            if asupan:
                asupan.delete_asupan_nutrisi()
                return True
            else:
                print(f"Asupan with ID {id} not found.")
                return False
        except Exception as e:
            print(f"Error deleting asupan nutrisi with ID {id}: {e}")
            return False
