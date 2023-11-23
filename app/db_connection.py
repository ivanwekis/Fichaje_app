import pymongo

class MongoDBConnection:
    def __init__(self, uri, database_name, collection_name):
        self.client = pymongo.MongoClient(uri)
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]

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
