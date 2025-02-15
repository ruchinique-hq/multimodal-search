import json

class CreatePreSignedUrlRequest:
    fingerprint: str
    file_name: str
    content_type: str

    def __init__(self, fingerprint: str, file_name: str, content_type: str):
        self.fingerprint = fingerprint
        self.file_name = file_name
        self.content_type = content_type

class ProcessingRequest:
    fingerprint: str
    key: str

    def __init__(self, fingerprint: str, key: str):
        self.fingerprint = fingerprint
        self.key = key

    def to_string(self) -> str:
        return json.dumps({
            "fingerprint": self.fingerprint,
            "key": self.key
        })