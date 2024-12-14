import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))


from src.data.database import connect_db, execute_query, fetch_all, fetch_one

class Latihan:
    def __init__(self,db_filename,id):
        self.db_filename = db_filename
        self._id = id
        self._nama = None
        self.get_latihan()

    def getId(self):
        return self._id

    def getNama(self):
        return self._nama
    
    def get_latihan(self):
        connection,cursor = connect_db(self.db_filename)

        query = "SELECT * FROM latihan WHERE id = ?"
        result = fetch_one(connection, cursor, query, (self._id,))

        if result:
            self._nama = result[1]

        connection.close()

class ListLatihan:
    def __init__(self,db_filename):
        self.db_filename = db_filename
        self._listLatihan = None
        self.latihan_data()

    def getListLatihan(self):
        return self._listLatihan
    
    def latihan_data(self):
        connection,cursor = connect_db(self.db_filename)

        query = "SELECT * FROM latihan "

        result = fetch_all(connection,cursor,query)

        if result:
            self._listLatihan = result
        
        connection.close()

# list = ListLatihan("src/data/data.db")
# print(list.getListLatihan())

# latihan = Latihan("src/data/data.db",20)
# print(latihan.getNama())


