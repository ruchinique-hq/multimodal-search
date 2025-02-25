from datetime import datetime
from typing import List, Optional
from bson import ObjectId

from models.search import Search, Question, QuestionStatus
from repositories.mongo_repository import MongoRepository
from constants.collection_names import SEARCH_COLLECTION, QUESTION_COLLECTION


class SearchRepository:
    def __init__(self, mongo_repository: MongoRepository):
        self.mongo_repository = mongo_repository

    def create_search(self, search_data: dict, created_by: str) -> Search:
        search_data["created_by"] = created_by
        search_data["updated_by"] = created_by
        search_data["created_date"] = datetime.now()
        search_data["updated_date"] = datetime.now()

        result = self.mongo_repository.insert_one(SEARCH_COLLECTION, search_data)
        search_data["_id"] = result.inserted_id

        return Search(**search_data)

    def get_search_by_id(self, search_id: ObjectId) -> Optional[Search]:
        result = self.mongo_repository.find_one(SEARCH_COLLECTION, {"_id": search_id})
        return Search(**result) if result else None

    def get_searches_by_asset(self, asset_id: ObjectId, page: int = 0, limit: int = 10) -> List[Search]:
        results = self.mongo_repository.find(
            SEARCH_COLLECTION,
            {"asset": asset_id},
            {"created_date": -1},
            page,
            limit
        )
        return [Search(**result) for result in results]

    def get_searches_by_created_by(self, created_by: str, page: int = 0, limit: int = 10) -> List[Search]:
        results = self.mongo_repository.find(
            SEARCH_COLLECTION,
            {"created_by": created_by},
            {"created_date": -1},
            page,
            limit
        )
        return [Search(**result) for result in results]


class QuestionRepository:
    def __init__(self, mongo_repository: MongoRepository):
        self.mongo_repository = mongo_repository

    def create_question(self, question_data: dict, created_by: str) -> Optional[Question]:
        question_data["status"] = QuestionStatus.PROCESSING.value
        question_data["created_date"] = datetime.now()
        question_data["updated_date"] = datetime.now()
        question_data["created_by"] = created_by
        question_data["updated_by"] = created_by

        result = self.mongo_repository.insert_one(QUESTION_COLLECTION, question_data)
        if result.inserted_id:
            question_data["_id"] = result.inserted_id
            return Question(**question_data)

        return None

    def update_question_answer(self, question_id: ObjectId, answer: str, token: int, updated_by: str) -> Optional[Question]:
        update_data = {
            "$set": {
                "answer": answer,
                "token": token,
                "status": QuestionStatus.ANSWERED.value,
                "updated_by": updated_by,
                "updated_date": datetime.now()
            }
        }
        result = self.mongo_repository.update_one(QUESTION_COLLECTION, {"_id": question_id}, update_data)
        if result.modified_count == 0:
            return None
        
        return self.get_question_by_id(question_id)

    def update_question_error(self, question_id: ObjectId, updated_by: str) -> Optional[Question]:
        update_data = {
            "$set": {
                "status": QuestionStatus.ERROR.value,
                "updated_by": updated_by,
                "updated_date": datetime.now()
            }
        }
        self.mongo_repository.update_one(QUESTION_COLLECTION, {"_id": question_id}, update_data)
        result = self.mongo_repository.find_one(QUESTION_COLLECTION, {"_id": question_id})
        return Question(**result) if result else None

    def get_questions_by_search(self, search_id: ObjectId, page: int = 0, limit: int = 10) -> List[Question]:
        results = self.mongo_repository.find(
            QUESTION_COLLECTION,
            {"search": search_id},
            {"created_date": -1},
            page,
            limit
        )
        return [Question(**result) for result in results]

    def get_question_by_id(self, question_id: ObjectId) -> Optional[Question]:
        result = self.mongo_repository.find_one(QUESTION_COLLECTION, {"_id": question_id})
        return Question(**result) if result else None
