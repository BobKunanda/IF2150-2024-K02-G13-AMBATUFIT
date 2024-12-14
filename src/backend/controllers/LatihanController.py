import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from src.backend.models.Latihan import Latihan, ListLatihan

class LatihanController:
    def __init__(self,db_filename,id):
        self.latihan_model = Latihan(db_filename,id)

    def get_latihan_data(self):
        try:
            latihan ={
                'id' : self.latihan_model.getId(),
                'nama': self.latihan_model.getNama()
            }
            return latihan
        except Exception as e:
            print(f"Terjadi kesalahan saat mengambil data latihan {e}")
            return None

class ListLatihanController:
    def __init__(self,db_filename):
        self.list_latihan = ListLatihan(db_filename)

    def get_list_latihan(self):
        try:
            listLatihan = []
            for id,nama in self.list_latihan.getListLatihan():
                latihan = {
                    'id':id,
                    'nama':nama
                }
                listLatihan.append(latihan)
            return listLatihan
        except Exception as e:
            print(f"Terjadi kesalahan saat mengambil list latihan: {e}")
            return None 


# controller = ListLatihanController("src/data/data.db")
# print(controller.get_list_latihan())