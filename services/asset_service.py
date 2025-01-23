from datetime import datetime
from enum import Enum

from repositories.asset_repositories import AssetRepository

from models.aws.s3_file_content import S3FileContent
from models.asset import Asset, Status

from logger import logger


class AssetService:
    def __init__(self, asset_repository: AssetRepository, processing_queue: str):
        self.asset_repository = asset_repository
        self.processing_queue = processing_queue

    def upload_asset(self, fingerprint: str, content: S3FileContent):

        logger.debug("uploading asset from s3 content")

        asset = {
            "name": content.file_name,
            "metadata": {
                "key": content.metadata.key,
                "etag": content.metadata.etag,
                "content_type": content.metadata.content_type,
                "content_length": content.metadata.content_length,
                "last_modified": content.metadata.last_modified
            },
            "created_date": datetime.now(),
            "updated_date": datetime.now(),
            "created_by": fingerprint,
            "updated_by": fingerprint,
            "status": Status.NEEDS_PROCESSING.value
        }

        asset = self.asset_repository.save(asset)
        if not asset:
            logger.error(f"asset not created for s3 content", content.metadata.key)
            return

        logger.info("asset created successfully")

        # triggering asset for processing after saved or updated
        self.trigger_processing(asset)

        logger.info(f"uploaded asset {asset.id} successfully")

    def trigger_processing(self, asset: Asset):
        try:

            logger.debug(f"triggering asset {asset.id} for processing")

            payload = {'id': asset.id}

            queue = self.get_queue_by_name(self.processing_queue)
            response = self.sqs.send_message(QueueUrl=queue['QueueUrl'], MessageBody=payload.__str__())

            logger.info(f"triggered asset {asset.id} for processing")

            return response

        except Exception as err:
            logger.error(f"failed trigger file for processing {err.__str__()}")

    def object_to_dict(self, obj):
        if isinstance(obj, dict):
            return {key: self.object_to_dict(value) for key, value in obj.items()}
        elif hasattr(obj, "__dict__"):
            return {key: self.object_to_dict(value) for key, value in obj.__dict__.items()}
        elif isinstance(obj, Enum):
            return obj.value
        elif isinstance(obj, datetime):
            return obj.isoformat()
        else:
            return obj
    