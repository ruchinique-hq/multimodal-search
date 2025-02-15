from datetime import datetime

from repositories.asset_repositories import AssetRepository

from services.amazon_service import AmazonService

from models.aws.s3_file_content import S3FileContent

from models.asset import Asset, Status
from models.requests.asset import SearchAssetRequest

from logger import logger


class AssetService:
    def __init__(self, asset_repository: AssetRepository, amazon_service: AmazonService, processing_queue: str):
        self.asset_repository = asset_repository
        self.amazon_service = amazon_service
        self.processing_queue = processing_queue

    def fetch_all(self, request: SearchAssetRequest) -> list[Asset]:
        return self.asset_repository.find_all({"created_by": request.fingerprint}, 
                                              {"created_date": -1}, 
                                              request.page, 
                                              request.limit)
    
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

        return self.asset_repository.save(asset)

    def trigger_processing(self, asset_id: str) -> None:
        queue = self.amazon_service.get_queue_by_name(self.processing_queue)
        self.amazon_service.sqs.send_message(QueueUrl=queue['QueueUrl'], MessageBody=asset_id)