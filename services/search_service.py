
from models.requests.search import SearchAnswerRequest

class SearchService:
    def __init__(self):
        pass

    def generate_answer(self, search_answer_request: SearchAnswerRequest):
        print('generating answer')