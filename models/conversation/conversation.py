from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from bson import ObjectId


class Conversation(BaseModel):
    id: ObjectId = Field("id", alias="_id")
    title: str = Field("title")
    assets: list[ObjectId] = Field("assets")
    created_date: datetime = Field("created_date")
    updated_date: datetime = Field("updated_date")
    created_by: str = Field("created_by")
    updated_by: str = Field("updated_by")
    
    model_config = ConfigDict(arbitrary_types_allowed=True)