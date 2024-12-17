class SearchAnswerResponse:
    query: str
    answer: str

    def __init__(self, query: str, answer: str):
        self.query = query
        self.answer = answer
