class SearchRequest:
    def __init__(self, asset: str, fingerprint: str, question: str):
        self.asset = asset
        self.question = question
        self.fingerprint = fingerprint
        
class FollowUpQuestionRequest:
    def __init__(self, search: str, question: str, fingerprint: str):
        self.search = search
        self.question = question
        self.fingerprint = fingerprint 
