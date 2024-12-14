import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))


from src.backend.models.SkemaLatihan import SkemaLatihan, ListSkemaLatihan, DetailSkemaLatihan, ListDetailSkemaLatihan

class SkemaController:
    def __init__(self,db_filename,idSkema = 0):
        self.skema_model = SkemaLatihan(db_filename,idSkema)

    def get_skema_data(self):
        try:
            self.skema_model.get_skema()
            skema = {
                'id' : self.skema_model.getId(),
                'nama': self.skema_model.getNama(),
                'deskripsi': self.skema_model.getDeskripsi(),
                'tipe': self.skema_model.getTipe(),
                'durasi': self.skema_model.getDurasi()
            }
            return skema
        except Exception as e:
            print(f"Terjadi kesalahan saat mengambil skema latihan {e}")
            return None
        
    def create_skema_data(self,data_dict):
        for key,value in data_dict.items():
            if hasattr(self.skema_model,f"set{key.capitalize()}"):
                setter = getattr(self.skema_model, f"set{key.capitalize()}")
                setter(value)


        self.skema_model.create_skema()

    def update_skema_data(self,data_dict):
        for key,value in data_dict.items():
            if hasattr(self.skema_model,f"set{key.capitalize()}"):
                setter = getattr(self.skema_model, f"set{key.capitalize()}")
                setter(value)
                
        self.skema_model.update_skema()

    def delete_skema_data(self):
        self.skema_model.delete_skema()

class ListSkemaController:
    def __init__(self,db_filename):
        self.list_skema = ListSkemaLatihan(db_filename)

    def get_list_skema(self):
        try:
            listSkema= []
            for id,nama,deskripsi,tipe,durasi in self.list_skema.getListSkema():
                skema = {
                    'id':id,
                    'nama':nama,
                    'deskripsi':deskripsi,
                    'tipe': tipe,
                    'durasi' : durasi
                }
                listSkema.append(skema)
            return listSkema
        except Exception as e:
            print(f"Terjadi kesalahan saat mengambil list skema: {e}")
            return None


class DetailSkemaController:
    def __init__(self, db_filename, id_urut = 0, id_skema = 0):
        self.detail_model = DetailSkemaLatihan(db_filename, id_urut, id_skema)

    def createDetailLatihan(self, data_detail):
        self.detail_model.set_id_latihan(data_detail['id_latihan'])
        self.detail_model.set_id_skema(data_detail['id_skema'])
        self.detail_model.set_reps(data_detail['reps'])
        self.detail_model.set_sets(data_detail['sets'])

        self.detail_model.createDetail()
    
    def deleteDetailLatihan(self):
        self.detail_model.deleteDetail()

class ListDetailController:
    def __init__(self, idSkema, db_filename):
        self._list_detail_model = ListDetailSkemaLatihan(db_filename,idSkema)

    def get_list_detail(self):
        try:
            listDetails = []

            for id_skema,id_urut,id_latihan,reps,sets in self._list_detail_model.getListDetail():
                detail = {
                    'id_skema' : id_skema,
                    'id_urut' : id_urut,
                    'id_latihan' : id_latihan,
                    'reps' : reps,
                    'sets' : sets
                }
                listDetails.append(detail)
            return listDetails
        
        except Exception as e:
            print(f"Terjadi kesalahan saat mengambil detail skema latihan {e}")
            return None
            
            
                

        


        

# controller = ListSkemaController("src/data/data.db")
# print(controller.get_list_skema())

     