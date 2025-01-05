from transformers import Qwen2VLForConditionalGeneration, AutoProcessor

import handlers

from dependency_injector import containers, providers

from repositories.mongo_repository import MongoRepository
from repositories.asset_repositories import AssetRepository

from services.search_service import SearchService
from services.amazon_service import AmazonService
from services.asset_service import AssetService
from config.app_config import read_config


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[handlers])

    config = read_config()

    model_local_path = "./documents/qwen2-vl"
    model = Qwen2VLForConditionalGeneration.from_pretrained(model_local_path, torch_dtype="auto", device_map="auto")
    processor = AutoProcessor.from_pretrained(model_local_path)

    mongo_repository = providers.Singleton(
        MongoRepository,
        config.mongo.uri,
        config.mongo.database
    )

    asset_repository = providers.Singleton(
        AssetRepository,
        mongo_repository
    )

    asset_service = providers.Singleton(
        AssetService,
        asset_repository
    )

    amazon_service = providers.Singleton(
        AmazonService,
        config.aws.access_key_id,
        config.aws.secret_access_key,
        config.aws.region,
        config.aws.bucket,
        config.aws.processing_queue
    )

    search_service = providers.Singleton(SearchService, amazon_service, model, processor)
