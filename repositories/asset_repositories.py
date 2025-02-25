from models.asset import Asset
from pymongo.results import InsertOneResult
from repositories.mongo_repository import MongoRepository

from constants.collection_names import ASSET_COLLECTION


class AssetRepository:
    def __init__(self, mongo_repository: MongoRepository):
        self.mongo_repository = mongo_repository

    def save(self, asset: dict) -> str:
        result: InsertOneResult = self.mongo_repository.insert_one(ASSET_COLLECTION, asset)
        return str(result.inserted_id)

    def find_one_by_id(self, asset_id: str):
        return self.mongo_repository.find_one(ASSET_COLLECTION, {"id": asset_id})
    
    def find_all(self, query: dict, sort: dict, page: int, limit: int) -> list[Asset]:
        documents = self.mongo_repository.find(ASSET_COLLECTION, query, sort, page, limit)
        if documents:
            return [Asset(**document) for document in documents]
        
        return []
