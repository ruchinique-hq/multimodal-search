from transformers import Qwen2VLForConditionalGeneration, AutoProcessor

import handlers

from dependency_injector import containers, providers

from repositories.conversation import conversation_repository
from repositories.conversation.conversation_repository import ConversationRepository
from repositories.conversation.chat_repository import ChatRepository
from repositories.mongo_repository import MongoRepository
from repositories.asset_repositories import AssetRepository

from repositories.search_repositories import SearchRepository, QuestionRepository

from services.search_service import SearchService
from services.amazon_service import AmazonService
from services.asset_service import AssetService
from config.app_config import read_config


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[handlers])

    config = read_config()

    # model_local_path = "./documents/qwen2-vl"
    # model = Qwen2VLForConditionalGeneration.from_pretrained(model_local_path, torch_dtype="auto", device_map="cpu")
    # processor = AutoProcessor.from_pretrained(model_local_path)

    model, processor = None, None

    mongo_repository = providers.Singleton(
        MongoRepository,
        config.mongo.uri,
        config.mongo.database
    )

    conversation_repository = providers.Singleton(
        ConversationRepository,
        mongo_repository
    )

    chat_repository = providers.Singleton(
        ChatRepository,
        mongo_repository
    )

    asset_repository = providers.Singleton(
        AssetRepository,
        mongo_repository
    )

    search_repository = providers.Singleton(
        SearchRepository,
        mongo_repository
    )

    question_repository = providers.Singleton(
        QuestionRepository,
        mongo_repository
    )

    amazon_service = providers.Singleton(
        AmazonService,
        config.aws.access_key_id,
        config.aws.secret_access_key,
        config.aws.region,
        config.aws.bucket
    )

    asset_service = providers.Singleton(
        AssetService,
        asset_repository,
        amazon_service,
        config.aws.processing_queue
    )

    search_service = providers.Singleton(SearchService, conversation_repository, chat_repository, amazon_service, model, processor)
