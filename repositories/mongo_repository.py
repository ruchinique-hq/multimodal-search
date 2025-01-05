from pymongo import MongoClient


class MongoRepository:
    def __init__(self, uri: str, database: str):
        self.client = MongoClient(uri)
        self.database = self.client[database]

    def create(self, collection: str, data: dict):
        self.database[collection].insert_one(data)

    def find_one(self, collection: str, query: dict):
        return self.database[collection].find_one(query)

    def find(self, collection: str, query: dict):
        return self.database[collection].find(query)

    def update_one(self, collection: str, query: dict, data: dict):
        return self.database[collection].update_one(query, data)
    
    def update_many(self, collection: str, query: dict, data: dict):
        return self.database[collection].update_many(query, data)

    def delete_one(self, collection: str, query: dict):
        return self.database[collection].delete_one(query)
    
    def delete_many(self, collection: str, query: dict):
        return self.database[collection].delete_many(query)
