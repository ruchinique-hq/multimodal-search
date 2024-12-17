from transformers import Qwen2VLForConditionalGeneration, AutoProcessor

import handlers

from dependency_injector import containers, providers

from services.search_service import SearchService
from config.app_config import read_config


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[handlers])

    config = read_config()

    model_local_path = "./documents/qwen2-vl"
    model = Qwen2VLForConditionalGeneration.from_pretrained(model_local_path, torch_dtype="auto", device_map="cpu")
    processor = AutoProcessor.from_pretrained(model_local_path)

    search_service = providers.Singleton(SearchService,model, processor)