import sys
import os

# Pastikan kita menambahkan path ke folder src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from src.backend.models.PersonalData import PersonalData

from .PersonalValidator import PersonalValidator

class ProfileController:
    def __init__(self, db_filename):
        """Inisialisasi controller dengan model profil yang diberikan."""
        self.profile_model = PersonalData(db_filename)

    def get_profile_data(self):
        """Mengambil data profil dari model menggunakan getter dan mengembalikannya dalam bentuk dictionary."""
        try:
            profile_data = {
                'nama': self.profile_model.getNama(),
                'usia': self.profile_model.getUsia(),
                'tinggi': self.profile_model.getTinggi(),
                'berat': self.profile_model.getBerat(),
                'tujuan': self.profile_model.getTujuan()
            }
            return profile_data
        except Exception as e:
            print(f"Terjadi kesalahan saat mengambil data profil: {e}")
            return None

    def update_profile_data(self, data_dict):
        """Memperbarui data profil dengan menerima data dictionary dan memvalidasinya."""
        try:
            for key, value in data_dict.items():
                # Validasi data sebelum diupdate
                if key == "usia":
                    if (value.isdigit()):
                        value = int(value)
                        PersonalValidator.validate_usia(value)
                    else:
                        print("Usia bukan integer")
                elif key == "tinggi":
                    if(self.is_real_number(value)):
                        value = float(value)
                        PersonalValidator.validate_tinggi(value)
                    else:
                        print("tinggi bukan real")
                elif key == "berat":
                    if(self.is_real_number(value)):
                        value = float(value)
                        PersonalValidator.validate_berat(value)
                    else:
                        print("berat bukan real")
                elif key == "tujuan":
                    PersonalValidator.validate_tujuan(value)

                if hasattr(self.profile_model, f"set{key.capitalize()}"):
                    # Memanggil setter berdasarkan key
                    setter = getattr(self.profile_model, f"set{key.capitalize()}")
                    setter(value)
            
            # Menyimpan perubahan ke database setelah update data
            self.profile_model.update_profile()
        except ValueError as ve:
            print(f"Kesalahan validasi: {ve}")
        except Exception as e:
            print(f"Terjadi kesalahan saat memperbarui profil: {e}")

    def is_real_number(self,s):
        try:
            float(s)  # Coba mengonversi string ke float
            return True
        except ValueError:
            return False
