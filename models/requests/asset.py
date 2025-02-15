class SearchAssetRequest:
    fingerprint: str
    page: int
    limit: int
    
    def __init__(self, fingerprint: str, page: int, limit: int):
        self.fingerprint = fingerprint
        self.page = page
        self.limit = limit

    def to_dict(self):
        return {"fingerprint": self.fingerprint}