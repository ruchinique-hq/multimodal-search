from models.asset import Metadata

class S3FileContent:
    file_name: str
    content: bytes
    metadata: Metadata

    def __init__(self, s3, bucket, key):
        try:
            response = s3.get_object(Bucket=bucket, Key=key)
            self.content = response['Body'].read()
            
            self.metadata = Metadata()
            self.metadata.key = key
            self.metadata.etag = response['ETag']
            self.metadata.content_length = response['ContentLength']
            self.metadata.content_type = response['ContentType']
            self.metadata.last_modified = response['LastModified']

            custom_metadata = response['Metadata']
            self.file_name = custom_metadata['file-name']

        except Exception as e:
            print(f"Error fetching object from S3: {e}")