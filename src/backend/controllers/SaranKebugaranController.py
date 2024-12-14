import os
import sys

from src.data.database import connect_db, execute_query, fetch_one, fetch_all
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from src.backend.models.SaranKebugaran import SaranKebugaran
from src.backend.controllers.PersonalDataController import ProfileController

class SaranKebugaranController:
    def __init__(self, db_filename):
        self.db_filename = db_filename
        self.saran_kebugaran_model = SaranKebugaran(db_filename)
        self.personal_data_controller = ProfileController(db_filename)

    def get_all_saran_kebugaran(self):
        """Mengambil semua saran kebugaran dari database."""
        return self.saran_kebugaran_model._load_all_saran_kebugaran()

    def get_saran_kebugaran_by_id(self, id):
        """Mengambil saran kebugaran berdasarkan ID."""
        return self.saran_kebugaran_model.load_saran_kebugaran(id)
    
    def get_corresponding_saran_kebugaran(self):
        # Mapper to convert tujuan to saran_kebugaran ID
        mapper = {
            "weight_loss": 1,
            "muscle_gain": 2,
            "fat_loss": 3,
            "rehabilitation": 4,
            "toning": 5,
            "maintain_weight": 6,
            "flexibility": 7,
            "strength": 8,
            "endurance": 9,
            "mobility": 10,
            "posture": 11,
            "mental_health": 12,
            "general_health": 13,
        }
        
        tujuan = self.personal_data_controller.get_profile_data()['tujuan']
        saran_kebugaran_id = mapper[tujuan]
        return self.get_saran_kebugaran_by_id(saran_kebugaran_id)