class SearchAnswerResponse:
    query: str
    answer: str

    def __init__(self, query: str, answer: str):
        self.query = query
        self.answer = answer

    def to_json(self):
        return {
            "query": self.query,
            "answer": self.answer
        }