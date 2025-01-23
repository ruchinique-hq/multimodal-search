from models.asset import Asset
from repositories.mongo_repository import MongoRepository

from constants.database import ASSETS_COLLECTION


class AssetRepository:
    def __init__(self, mongo_repository: MongoRepository):
        self.mongo_repository = mongo_repository

    def save(self, asset: dict) -> Asset:
        document = self.mongo_repository.insert_one(ASSETS_COLLECTION, asset)
        if document:
            return Asset(**document)

    def find_one_by_id(self, asset_id: str):
        return self.mongo_repository.find_one(ASSETS_COLLECTION, {"id": asset_id})
