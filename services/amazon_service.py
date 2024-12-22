import boto3
import uuid

from botocore.exceptions import ClientError
from models.requests.file import CreatePreSignedUrlRequest
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

        self.bucket = bucket

    def generate_pre_signed_url(self, request: CreatePreSignedUrlRequest) -> dict | None:
        try:

            logger.debug(f"generating pre-signed url for {request.file_name}")

            key = request.fingerprint + "/" + str(uuid.uuid4())
            fields = {'Content-Type': request.content_type}
            conditions = [["eq", "$Content-Type", request.content_type]]

            response = self.s3.generate_presigned_post(Bucket=self.bucket,
                                                       Key=key,
                                                       ExpiresIn=3600,
                                                       Fields=fields,
                                                       Conditions=conditions)

            logger.info(f"generated pre-signed url for {request.file_name}")
            return response

        except ClientError as e:
            logger.error(f"failed to generate pre-signed url for {request.file_name} {e.__str__()}")
