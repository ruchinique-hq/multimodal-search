from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict

class Metadata:
    key: str
    etag: str
    content_length: int
    content_type: str
    last_modified: str

    # add config to class Metadata


class Status(Enum):
    NEEDS_PROCESSING = "NEEDS_PROCESSING"
    PROCESSED = "PROCESSED"
    ERROR = "ERROR"

class Asset(BaseModel):
    id: str = Field("id", alias="_id")
    name: str = Field("name")
    created_date: datetime = Field("created_date")
    created_by: str = Field("created_by")
    updated_date: datetime = Field("updated_date")
    updated_by: str = Field("updated_by")
    status: Status = Field("status")
    metadata: Metadata = Field("metadata")

    model_config = ConfigDict(arbitrary_types_allowed=True)
