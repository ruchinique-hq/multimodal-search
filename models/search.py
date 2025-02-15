from datetime import datetime
from enum import Enum
from bson import ObjectId
from pydantic import BaseModel, Field, ConfigDict


class QuestionStatus(Enum):
    PROCESSING = "PROCESSING"
    ANSWERED = "ANSWERED"
    ERROR = "ERROR"


class Search(BaseModel):
    id: ObjectId = Field(alias="_id")
    title: str = Field("title")
    asset: ObjectId = Field("asset")  
    created_date: datetime = Field("created_date")
    updated_date: datetime = Field("updated_date")
    created_by: str = Field("created_by")
    updated_by: str = Field("updated_by")

    model_config = ConfigDict(arbitrary_types_allowed=True)


class Question(BaseModel):
    id: ObjectId = Field(alias="_id")
    search: ObjectId = Field("search")
    asset: ObjectId = Field("asset")
    question: str = Field("question")
    answer: str = Field("answer")
    token: int = Field("token", default_factory=int)
    status: QuestionStatus = Field("status", default_factory=QuestionStatus.PROCESSING)
    created_date: datetime = Field("created_date", default_factory=datetime.now)
    updated_date: datetime = Field("updated_date", default_factory=datetime.now)
    created_by: str = Field("created_by")
    updated_by: str = Field("updated_by")

    model_config = ConfigDict(arbitrary_types_allowed=True)