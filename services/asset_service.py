from datetime import datetime

from bson import ObjectId

from models.aws.s3_file_content import S3FileContent
from models.asset.asset import Asset, Status

from repositories.asset.asset_repository import AssetRepository
from repositories.asset.asset_transaction_repository import AssetTransactionRepository

from services.amazon_service import AmazonService

from logger import logger


class AssetService:
    def __init__(self, asset_repository: AssetRepository, asset_transaction_repository: AssetTransactionRepository,amazon_service: AmazonService, processing_queue: str):
        self.asset_repository = asset_repository
        self.asset_transaction_repository = asset_transaction_repository
        self.amazon_service = amazon_service
        self.processing_queue = processing_queue
    
    def create_asset(self, fingerprint: str, content: S3FileContent) -> str:
        
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

        return self.asset_repository.create_asset(asset, fingerprint)

    def trigger_processing(self, asset_id: str) -> None:
        queue = self.amazon_service.get_queue_by_name(self.processing_queue)
        response = self.amazon_service.sqs.send_message(QueueUrl=queue['QueueUrl'], MessageBody=asset_id)
        self.create_transaction_for_asset(asset_id, response['MessageId'], fingerprint)

    def create_transaction_for_asset(self, asset_id: str, message_id: str, created_by: str) -> str:
        data = {"asset": ObjectId(asset_id), "message_id": message_id}
        return self.asset_transaction_repository.create_transaction(data, created_by)
    
