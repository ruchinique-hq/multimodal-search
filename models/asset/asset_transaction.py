from bson import ObjectId
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class AssetProcessingTransaction(BaseModel):
    id: ObjectId = Field(alias="_id")
    asset: ObjectId = Field("asset")
    message_id: str = Field("message_id")
    created_date: datetime = Field("created_date")
    updated_date: datetime = Field("updated_date")
    created_by: str = Field("created_by")
    updated_by: str = Field("updated_by")

    model_config = ConfigDict(arbitrary_types_allowed=True)