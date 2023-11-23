from pymongo.mongo_client import MongoClient
from urllib.parse import quote_plus
import ssl

class MongoDBConnection:
    def __init__(self, db_user, uri_password, database_name, collection_name):
        db_user = quote_plus(db_user)
        uri_password = quote_plus(uri_password)
        uri = f"mongodb+srv://{db_user}:{uri_password}@cluster0.srdnijs.mongodb.net/"
        self.client = MongoClient(uri, ssl=True)
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]
        self._start_connection()

    def _start_connection(self):
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

    def find_user(self, filtro):
        return self.collection.find_one(filtro)

    def insert_user(self, usuario):
        # Inserta un nuevo usuario en la colección
        return self.collection.insert_one(usuario)

    def update_user(self, filtro, nuevo_valor):
        # Actualiza la información de un usuario que cumple con el filtro
        return self.collection.update_one(filtro, {"$set": nuevo_valor})

    def delete_user(self, filtro):
        # Elimina un usuario que cumple con el filtro
        return self.collection.delete_one(filtro)

    def close_connection(self):
        self.client.close()
