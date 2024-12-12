import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from src.data.database import connect_db, execute_query, fetch_one,fetch_all



class SkemaLatihan:
    def __init__(self,db_filename,id=0):
        self.db_filename = db_filename
        self._id = id
        self._nama = None
        self._deskripsi = None
        self._tipe = None
        self._durasi = None

    def getId(self):
        return self._id
    
    def setId(self, id):
        self._id = id

    def getNama(self):
        return self._nama

    def setNama(self, nama):
        self._nama = nama

    def getDeskripsi(self):
        return self._deskripsi

    def setDeskripsi(self, deskripsi):
        self._deskripsi = deskripsi

    def getTipe(self):
        return self._tipe

    def setTipe(self, tipe):
        self._tipe = tipe

    def getDurasi(self):
        return self._durasi

    def setDurasi(self, durasi):
        self._durasi = durasi
    
    def create_skema(self):
        connection, cursor = connect_db(self.db_filename)

        query = """
            INSERT INTO skema_latihan (nama,deskripsi,tipe,durasi)
            VALUES (?, ?, ?, ?)
        """
        params = (self._nama,self._deskripsi,self._tipe,self._durasi)



        execute_query(connection,cursor,query,params)

        self.setId(cursor.lastrowid)
        connection.close()

    def update_skema(self):
        connection, cursor = connect_db(self.db_filename)

        query = """
            UPDATE skema_latihan
            SET nama = ?, deskripsi = ?, tipe = ?, durasi = ?
            WHERE id = ?
        """
        params = (self._nama, self._deskripsi, self._tipe, self._durasi, self._id)

        execute_query(connection,cursor,query,params)

        connection.close()

    def delete_skema(self):
        connection, cursor = connect_db(self.db_filename)

        query = """
            DELETE FROM skema_latihan WHERE id = ?;
        """
        params = (self._id,)


        execute_query(connection,cursor,query,params)

        query2 = """
            DELETE FROM detail_skema_latihan WHERE id_skema = ?; 
        """

        execute_query(connection,cursor,query2,params)

        connection.close()

    def get_skema(self):
        connection, cursor = connect_db(self.db_filename)

        query = """
            SELECT * FROM skema_latihan WHERE id = ?
        """
        params = (self._id,)

        result = fetch_one(connection,cursor,query,params)

        if result:
            self._nama = result[1]
            self._deskripsi = result[2]
            self._tipe = result[3]
            self._durasi = result[4]

        
        connection.close()


class ListSkemaLatihan:
    def __init__(self, db_filename):
        self.db_filename = db_filename
        self._listSkema = None

    def getListSkema(self):

        connection,cursor = connect_db(self.db_filename)

        query = "SELECT * FROM skema_latihan "

        result = fetch_all(connection,cursor,query)

        if result:
            self._listSkema = result
        
        connection.close()

        return self._listSkema        
    
class DetailSkemaLatihan:
    def __init__(self, db_filename, id_urut = 0, id_skema = 0):
        self.db_filename = db_filename
        self._id_skema = id_skema
        self._id_urut = id_urut
        self._id_latihan = None
        self._reps = None
        self._sets = None

    def get_id_skema(self):
        return self._id_skema

    def set_id_skema(self, value):
        self._id_skema = value

    def get_id_urut(self):
        return self._id_urut

    def set_id_urut(self, value):
        self._id_urut = value

    def get_id_latihan(self):
        return self._id_latihan

    def set_id_latihan(self, value):
        self._id_latihan = value

    def get_reps(self):
        return self._reps

    def set_reps(self, value):
        self._reps = value

    def get_sets(self):
        return self._sets

    def set_sets(self, value):
        self._sets = value

    def createDetail(self):
        connection,cursor = connect_db(self.db_filename)

        query_get_max = "SELECT MAX(id_urut) FROM detail_skema_latihan WHERE id_skema = ?"
        cursor.execute(query_get_max, (self._id_skema,))
        result = cursor.fetchone()
        max_id_urut = result[0] if result[0] is not None else 0 

        new_id_urut = max_id_urut + 1

        query = """INSERT INTO detail_skema_latihan (id_skema, id_urut, id_latihan, reps, sets)
                    VALUES (?, ?, ?, ?, ?)
                """

        params = (self._id_skema, new_id_urut, self._id_latihan, self._reps, self._sets)

        execute_query(connection,cursor,query,params)

        connection.close()

    def deleteDetail(self):
        connection,cursor = connect_db(self.db_filename)

        query = """
            DELETE FROM detail_skema_latihan WHERE id_urut = ? AND id_skema = ?; 
        """
        params = (self._id_urut, self._id_skema)

        execute_query(connection,cursor,query,params)

        connection.close()

        


class ListDetailSkemaLatihan:
    def __init__(self, db_filename, idSkema):
        self.db_filename = db_filename
        self._idSkema = idSkema
        self._list_detail = None
    
    def getListDetail(self):
        connection,cursor = connect_db(self.db_filename)

        query = "SELECT * FROM detail_skema_latihan WHERE id_skema = ?"

        params = (self._idSkema,)

        result = fetch_all(connection,cursor,query,params)

        if result:
            self._list_detail = result
        
        connection.close()

        return self._list_detail     
        
        
# list = ListSkemaLatihan("src/data/data.db")
# print(list.getListSkema())

# skema = SkemaLatihan("src/data/data.db",3)
# skema.get_skema()
# print(skema.getTipe())

# list = DetailSkemaLatihan("src/data/data.db",2)
# print(list.getListDetail())
