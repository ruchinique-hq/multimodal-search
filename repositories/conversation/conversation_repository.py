from bson import ObjectId
from typing import Optional
from datetime import datetime

from models.conversation.conversation import Conversation
from repositories.mongo_repository import MongoRepository

from constants.collection_names import CONVERSATION_COLLECTION


class ConversationRepository:
    def __init__(self, mongo_repository: MongoRepository):
        self.mongo_repository = mongo_repository

    def create_conversation(self, data: dict, fingerprint: str) -> str:
        data.update({
            "created_by": fingerprint,
            "updated_by": fingerprint,
            "created_date": datetime.now(),
            "updated_date": datetime.now()
        })

        result = self.mongo_repository.insert_one(CONVERSATION_COLLECTION, data)
        return str(result.inserted_id)

    def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        result = self.mongo_repository.find_one(CONVERSATION_COLLECTION, {"_id": ObjectId(conversation_id)})
        return Conversation(**result) if result else None

    def update_conversation(self, conversation_id: str, update_data: dict) -> bool:
        result = self.mongo_repository.update_one(CONVERSATION_COLLECTION, {"_id": ObjectId(conversation_id)}, {"$set": update_data})
        return result.modified_count > 0

    def delete_conversation(self, conversation_id: str) -> bool:
        result = self.mongo_repository.delete_one(CONVERSATION_COLLECTION, {"_id": ObjectId(conversation_id)})
        return result.deleted_count > 0