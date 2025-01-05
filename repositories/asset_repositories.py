from models.asset import Asset
from repositories.mongo_repository import MongoRepository

from constants.database import ASSETS_COLLECTION


class AssetRepository:
    def __init__(self, mongo_repository: MongoRepository):
        self.mongo_repository = mongo_repository

    def create_asset(self, asset: Asset):
        self.mongo_repository.create(ASSETS_COLLECTION, asset.model_dump())

    def get_asset(self, asset_id: str):
        return self.mongo_repository.find_one(ASSETS_COLLECTION, {"id": asset_id})
