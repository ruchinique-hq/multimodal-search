class SearchAnswerRequest:
    query: str

    def __init__(self, query: str):
        self.query = query