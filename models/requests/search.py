from pydantic import BaseModel, Field
from typing import Optional

class GetAnswerRequest(BaseModel):
    asset: str
    question: str
    fingerprint: str
    conversation: Optional[str] = None