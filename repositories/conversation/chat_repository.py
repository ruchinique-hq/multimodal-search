from typing import Optional
from datetime import datetime
from bson import ObjectId

from models.conversation.chat import Chat

from repositories.mongo_repository import MongoRepository

from constants.collection_names import CHAT_COLLECTION


class ChatRepository:
    def __init__(self, mongo_repository: MongoRepository):
        self.mongo_repository = mongo_repository

    def create_chat(self, data: dict, fingerprint: str) -> str:
        data.update({
            "created_by": fingerprint,
            "updated_by": fingerprint,
            "created_date": datetime.now(),
            "updated_date": datetime.now()
        })

        result = self.mongo_repository.insert_one(CHAT_COLLECTION, data)
        return str(result.inserted_id)

    def get_chat(self, chat_id: str) -> Optional[Chat]:
        result = self.mongo_repository.find_one(CHAT_COLLECTION, {"_id": ObjectId(chat_id)})
        return Chat(**result) if result else None

    def update_chat(self, chat_id: str, update_data: dict) -> bool:
        result = self.mongo_repository.update_one(CHAT_COLLECTION, {"_id": ObjectId(chat_id)}, update_data)
        return result.modified_count > 0

    def delete_chat(self, chat_id: str) -> bool:
        result = self.mongo_repository.delete_one(CHAT_COLLECTION, {"_id": ObjectId(chat_id)})
        return result.deleted_count > 0