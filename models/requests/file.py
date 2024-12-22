class CreatePreSignedUrlRequest:
    fingerprint: str
    file_name: str
    content_type: str

    def __init__(self, fingerprint: str, file_name: str, content_type: str):
        self.fingerprint = fingerprint
        self.file_name = file_name
        self.content_type = content_type

class ProcessingRequest:
    key: str

    def __init__(self, key: str):
        self.key = key