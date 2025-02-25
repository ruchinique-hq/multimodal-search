from typing import Optional
import boto3
import uuid

from botocore.exceptions import ClientError

from models.aws.s3_file_content import S3FileContent
from models.requests.file import CreateSignedUrlRequest

from logger import logger

PRE_SIGNED_URL_EXPIRATION = 3600


class AmazonService:
    def __init__(self, access_key: str, secret_key: str, region: str, bucket: str):

        self.s3 = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )

        self.sqs = boto3.client(
            'sqs',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )

        self.bucket = bucket

    def get_queue_by_name(self, name: str):
        return self.sqs.get_queue_url(QueueName=name)

    def generate_pre_signed_url(self, request: CreateSignedUrlRequest) -> Optional[dict]:
        try:
            logger.debug(f"generating pre-signed URL for {request.file_name}")
            
            key = f"{request.fingerprint}/{uuid.uuid4()}/{request.file_name}"
            fields = {'Content-Type': request.content_type, 'x-amz-meta-file-name': request.file_name}
            conditions = [
                ["eq", "$Content-Type", request.content_type],
                ["eq", "$x-amz-meta-file-name", request.file_name],
            ]

            return self.s3.generate_presigned_post(
                Bucket=self.bucket,
                Key=key,
                ExpiresIn=PRE_SIGNED_URL_EXPIRATION,
                Fields=fields,
                Conditions=conditions
            )

        except ClientError as e:
            logger.error(f"Failed to generate pre-signed URL for {request.file_name}: {e}")
        
        return None

    def get_object(self, key: str) -> S3FileContent:
        return S3FileContent(self.s3, self.bucket, key)

