import boto3
import uuid

from botocore.exceptions import ClientError
from models.requests.file import CreatePreSignedUrlRequest, ProcessingRequest
from logger import logger

PRE_SIGNED_URL_EXPIRATION = 3600


class AmazonService:
    def __init__(self, access_key: str, secret_key: str, region: str, bucket: str, processing_queue: str):

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
        self.processing_queue = processing_queue

    def get_queue_by_name(self, processing_queue: str):
        return self.sqs.get_queue_url(QueueName=processing_queue)

    def generate_pre_signed_url(self, request: CreatePreSignedUrlRequest) -> dict | None:
        try:

            logger.debug(f"generating pre-signed url for {request.file_name}")

            key = self.generate_key(request)
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

    def trigger_processing(self, request: ProcessingRequest):
        try:

            logger.debug(f"trigger file {request.key} for processing")

            queue = self.get_queue_by_name(self.processing_queue)
            response = self.sqs.send_message(QueueUrl=queue['QueueUrl'], MessageBody=request.key)

            logger.info(f"triggered file {request.key} for processing")
            return response

        except Exception as err:
            logger.error(f"failed trigger file for processing {err.__str__()}")

    def generate_key(self, request: CreatePreSignedUrlRequest):
        return request.fingerprint + "/" + str(uuid.uuid4()) + "/" + request.file_name