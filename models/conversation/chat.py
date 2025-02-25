from bson import ObjectId
from pydantic import BaseModel
from datetime import datetime
from pydantic import BaseModel, Field
from pydantic.config import ConfigDict


class Chat(BaseModel):
    id: ObjectId = Field("id", alias="_id")
    question: str = Field("question")
    answer: str = Field("answer")
    conversation: ObjectId = Field("conversation")
    assets: list[ObjectId] = Field("assets")
    token: int = Field("token")
    created_date: datetime = Field("created_date")
    updated_date: datetime = Field("updated_date")
    created_by: str = Field("created_by")
    updated_by: str = Field("updated_by")

    model_config = ConfigDict(arbitrary_types_allowed=True)