from pymongo.mongo_client import MongoClient
from urllib.parse import quote_plus
import logging

log = logging.getLogger(__name__)


class MongoDBConnection:
    def __init__(self, db_user, uri_password, database_name, collection_name=None):
        db_user = quote_plus(db_user)
        uri_password = quote_plus(uri_password)
        uri = f"mongodb+srv://{db_user}:{uri_password}@cluster0.srdnijs.mongodb.net/"
        self.client = MongoClient(uri, ssl=True)
        self.db = self.client[database_name]

        if collection_name is not None:
            self.collection = self.db[collection_name]
            self._ping()

    def _ping(self):
        try:
            self.client.admin.command("ping")
            log.info("Pinged your deployment. You successfully connected to MongoDB!")
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

    def _set_collection(self, collection_name):
        self.collection = self.db[collection_name]

    def find_user(self, filtro):
        return self.collection.find_one(filtro)

    def insert_user(self, usuario):
        # Inserta un nuevo usuario en la colección
        return self.collection.insert_one(usuario)

    def insert_register(self, usuario):
        # Inserta un nuevo usuario en la colección
        return self.collection.insert_one(usuario)

    def more_than_one(self, filter, new_value):
        # Update a register that matches the filter
        return self.collection.update_one(filter, new_value)

    def update_one_register(self, filtro, nuevo_valor):
        # Actualiza la información de un usuario que cumple con el filtro
        return self.collection.update_one(filtro, {"$set": nuevo_valor})

    def search_registers(self):
        return self.collection.find()

    def update_user(self, filtro, nuevo_valor):
        # Actualiza la información de un usuario que cumple con el filtro
        return self.collection.update_one(filtro, {"$set": nuevo_valor})

    def delete_user(self, filtro):
        # Elimina un usuario que cumple con el filtro
        return self.collection.delete_one(filtro)

    def registers_length(self):
        return self.collection.count_documents({})

    def find_12_sort_by_date(self, filtro, page):
        return (
            self.collection.find(filtro).sort("_id", -1).limit(12).skip(12 * (page - 1))
        )

    def insert_documents(self, documents):
        # Inserta varios documentos en la colección
        return self.collection.insert_many(documents)

    def close_connection(self):
        self.client.close()
