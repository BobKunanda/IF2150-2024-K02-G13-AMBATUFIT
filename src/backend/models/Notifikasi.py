import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from src.data.database import connect_db, execute_query, fetch_one,fetch_all



class Notifikasi:
    def __init__(self,db_filename):
        self._id = None
        self._nama = None
        self._waktu = None
        self._db_filename = db_filename

    def getId(self):
        return self._id
    
    def getNama (self):
        return self._nama
    
    def getWaktu(self):
        return self._waktu
    
    def setId(self,value):
        self._id = value
    
    def setNama(self,value):
        self._nama = value

    def setWaktu(self,value):
        self._waktu = value

    def createNotifikasi(self):
        connection, cursor = connect_db(self._db_filename)

        query = """
            INSERT INTO notifikasi (nama,waktu)
            VALUES (?, ?)
        """
        params = (self._nama, self._waktu)

        execute_query(connection,cursor,query,params)

        connection.close()

    def updateNotifikasi(self):
        connection, cursor = connect_db(self._db_filename)

        query = """
            UPDATE notifikasi
            SET nama = ?, waktu = ?
            WHERE id = ?
        """
        params = (self._nama, self._waktu, self._id)

        execute_query(connection,cursor,query,params)

        connection.close()

    def deleteNotifikasi(self):
        connection, cursor = connect_db(self._db_filename)

        query = """
            DELETE FROM notifikasi WHERE id = ?
        """
        params = (self._id,)

        execute_query(connection,cursor,query,params)

        connection.close()

    def getNotifikasi(self):
        connection, cursor = connect_db(self._db_filename)

        query = """
            SELECT * FROM notifikasi where id = ?
        """
        params = (self._id,)

        result = fetch_one(connection,cursor,query,params)

        if result:
            self._id = result[0]
            self._nama = result[1]
            self._waktu = result[2]
        connection.close()

class ListNotifikasi:
    def __init__(self, db_filename):
        self._db_filename = db_filename
        self._listNotifikasi = None

    def getListNotifikasi(self):
        connection, cursor = connect_db(self._db_filename)

        query = """
            SELECT * FROM notifikasi
        """
        

        result = fetch_all(connection,cursor,query)

        
        if result:
            self._listNotifikasi = result
        else:
            self._listNotifikasi = None
        connection.close()

        return self._listNotifikasi

# list = ListNotifikasi("src/data/data.db")
# print(list.getListNotifikasi())