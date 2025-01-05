import datetime
from enum import Enum


class Status(Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class Asset:
    id: str
    name: str
    key: str
    fingerprint: str
    created_date: datetime
    updated_date: datetime
    status: Status
    metadata: dict

    def __init__(self, id: str, name: str, key: str, fingerprint: str, created_date: datetime, updated_date: datetime, status: Status, metadata: dict):
        self.id = id
        self.name = name
        self.key = key
        self.fingerprint = fingerprint
        self.created_date = created_date
        self.updated_date = updated_date
        self.status = status
        self.metadata = metadata


