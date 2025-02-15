from models.asset import Metadata
from datetime import datetime
from typing import Optional


class S3FileContent:
    file_name: Optional[str]
    content: bytes
    metadata: Metadata

    def __init__(self, s3, bucket: str, key: str):
        try:
            response = s3.get_object(Bucket=bucket, Key=key)

            # Read content
            self.content = response['Body'].read()

            # Extract metadata
            self.metadata = Metadata(
                key=key,
                etag=response.get('ETag', ''),
                content_length=response.get('ContentLength', 0),
                content_type=response.get('ContentType', ''),
                last_modified=response.get('LastModified', datetime.min)
            )

            # Extract file name from custom metadata if available
            self.file_name = response.get('Metadata', {}).get('file-name', None)

        except Exception as e:
            print(f"Unexpected error fetching object from S3: {e}")