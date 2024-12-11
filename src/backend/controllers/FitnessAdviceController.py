import sys
import os

# Pastikan kita menambahkan path ke folder src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from src.backend.models.FitnessAdvice import FitnessAdvice
from src.backend.models.PersonalData import PersonalData

class ProfileController:
    def __init__(self, db_filename):
        """Inisialisasi controller dengan model saran kebugaran yang diberikan."""
        self.advice_model = FitnessAdvice(db_filename)
        self.personal_model = PersonalData(db_filename)
    def get_fitness_advice(self):
        try:
            personal_data = {
                'nama': self.personal_model.getNama(),
                'usia': self.personal_model.getUsia(),
                'tinggi': self.personal_model.getTinggi(),
                'berat': self.personal_model.getBerat(),
                'tujuan': self.personal_model.getTujuan()
            }

            # INI NANTI DIBENERIN SETELAH FITUR ASUPAN NUTRISI
            nutrient_data = get_nutrient_data(self.advice_model.db_filename)

            # INI JUGA
            advice = self.generate_fitness_advice(nutrient_data, personal_data)

            self.advice_model.set_id(1)
            self.advice_model.set_saran_latihan(advice['saran_latihan'])
            self.advice_model.set_saran_nutrisi(advice['saran_nutrisi'])
            self.advice_model.update_advice()

            return advice

        except Exception as e:
            return None

    def generate_fitness_advice(self, nutrient_data, personal_data: PersonalData):
        advice = {"saran_latihan": "", "saran_nutrisi": ""}

        # INI NANTI DIBENERIN SETELAH FITUR ASUPAN NUTRISI
        carb_threshold = 150
        protein_threshold = 70
        fat_threshold = 50

        # Generate advice based on nutrient levels
        if get_nutrient_data("carbs", 0) < carb_threshold:
            advice["saran_latihan"] = "Fokus pada olahraga ringan seperti yoga atau berjalan kaki."
            advice["saran_nutrisi"] = "Tambahkan asupan karbohidrat sehat seperti nasi merah atau ubi."
        elif get_nutrient_data("protein", 0) < protein_threshold:
            advice["saran_latihan"] = "Lakukan latihan kekuatan untuk meningkatkan massa otot."
            advice["saran_nutrisi"] = "Konsumsi lebih banyak protein dari daging tanpa lemak atau kacang-kacangan."
        else:
            advice["saran_latihan"] = "Anda siap untuk latihan intensitas tinggi seperti HIIT atau angkat beban."
            advice["saran_nutrisi"] = "Pertahankan pola makan seimbang."

        goal = personal_data.getTujuan().lower()
        if goal == "weight_loss":
            advice["saran_nutrisi"] += " Kurangi sedikit asupan lemak dan pilih makanan rendah kalori."
        elif goal == "muscle_gain":
            advice["saran_latihan"] += " Fokus pada progressive overload dalam latihan kekuatan."
            advice["saran_nutrisi"] += " Tambahkan kalori dari sumber sehat untuk mendukung pertumbuhan otot."
        elif goal == "cardio_fitness":
            advice["saran_latihan"] += " Prioritaskan latihan kardio seperti lari atau bersepeda."

        return advice

