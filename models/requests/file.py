from pydantic import BaseModel

class CreateSignedUrlRequest(BaseModel):
    fingerprint: str
    file_name: str
    content_type: str

class ProcessFileRequest(BaseModel):
    fingerprint: str
    key: str