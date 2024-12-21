import boto3

from botocore.exceptions import ClientError

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

    def generate_pre_signed_url(self, fingerprint: str, file_name: str) -> str | None:
        try:

            logger.debug(f"generating pre-signed url for {file_name}")

            key: str = self.generate_key(fingerprint, file_name)
            
            params = {'Bucket': self.bucket, 'Key': key}
            presigned_url = self.s3.generate_presigned_url('put_object', Params=params, ExpiresIn=PRE_SIGNED_URL_EXPIRATION)

            logger.info(f"generated pre-signed url for {file_name}")
            return presigned_url

        except ClientError as e:
            logger.error(f"failed to generate pre-signed url for {file_name} {e.__str__()}")

    def generate_key(self, fingerprint: str, file_name: str) -> str:
        return  fingerprint + "/" + file_name

