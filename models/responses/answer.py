from pydantic import BaseModel, Field

class SearchAnswerResponse(BaseModel):
    id: str = Field(...)
    conversation: str = Field(...)
    question: str = Field(...)
    answer: str = Field(...)
    token: int = Field(...)