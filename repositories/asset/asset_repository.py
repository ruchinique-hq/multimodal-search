from datetime import datetime
from bson import ObjectId


from constants.collection_names import ASSET_COLLECTION

from models.asset.asset import Asset
from repositories.mongo_repository import MongoRepository

class AssetRepository:
    def __init__(self, mongo_repository: MongoRepository):
        self.mongo_repository = mongo_repository

    def create_asset(self, data: dict, created_by: str) -> Asset:
        data['created_by'] = created_by
        data['updated_by'] = created_by
        data['created_date'] = datetime.now()
        data['updated_date'] = datetime.now()

        result = self.mongo_repository.insert_one(ASSET_COLLECTION, data)
        return Asset(**data, id=result.inserted_id)

    def get_asset(self, asset_id: str) -> Asset:
        asset = self.mongo_repository.find_one(ASSET_COLLECTION, {"_id": ObjectId(asset_id)})
        return Asset(**asset) if asset else None

    def update_asset(self, asset_id: str, update_data: dict, updated_by: str) -> bool:
        update_data['updated_by'] = updated_by
        update_data['updated_date'] = datetime.now()

        result = self.mongo_repository.update_one(
            ASSET_COLLECTION,
            {"_id": ObjectId(asset_id)},
            {"$set": update_data}
        )

        return result.modified_count > 0

    def delete_asset(self, asset_id: str) -> bool:
        result = self.mongo_repository.delete_one(ASSET_COLLECTION, {"_id": ObjectId(asset_id)})
        return result.deleted_count > 0
