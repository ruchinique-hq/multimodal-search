from datetime import datetime
from bson import ObjectId
from typing import Optional

from constants.collection_names import ASSET_TRANSACTION_COLLECTION

from models.asset.asset_transaction import AssetProcessingTransaction
from repositories.mongo_repository import MongoRepository


class AssetTransactionRepository:
    def __init__(self, mongo_repository: MongoRepository):
        self.mongo_repository = mongo_repository

    def create_transaction(self, data: dict, created_by: str) -> str:
        data['created_by'] = created_by
        data['updated_by'] = created_by
        data['created_date'] = datetime.now()
        data['updated_date'] = datetime.now()

        result = self.mongo_repository.insert_one(ASSET_TRANSACTION_COLLECTION, data)
        return str(result.inserted_id)

    def get_transaction(self, transaction_id: str) -> Optional[AssetProcessingTransaction]:
        query = {"_id": ObjectId(transaction_id)}
        result = self.mongo_repository.find_one(ASSET_TRANSACTION_COLLECTION, query)
        return AssetProcessingTransaction(**result) if result else None

    def update_transaction(self, transaction_id: str, update_data: dict, updated_by: str) -> bool:
        query = {"_id": ObjectId(transaction_id)}
        update_data['updated_by'] = updated_by
        update_data['updated_date'] = datetime.now()

        result = self.mongo_repository.update_one(ASSET_TRANSACTION_COLLECTION, query, {"$set": update_data})
        return result.modified_count > 0
    
    def delete_transaction(self, transaction_id: str) -> bool:
        query = {"_id": ObjectId(transaction_id)}
        result = self.mongo_repository.delete_one(ASSET_TRANSACTION_COLLECTION, query)
        return result.deleted_count > 0
    