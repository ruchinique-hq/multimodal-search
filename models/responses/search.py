class SearchResponse:
    search: str
    asset: str
    question: str
    answer: str
    token: int
    status: str
    created_by: str
    updated_by: str
    created_date: datetime
    updated_date: datetime

    def to_dict(self) -> dict:
        return {
            "search": self.search,
            "asset": self.asset,
            "question": self.question,
            "answer": {
                "text": self.answer,
                "token": self.token
            },
            "status": self.status
        }