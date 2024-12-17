import handlers

from dependency_injector import containers, providers

from services.search_service import SearchService
from config.app_config import read_config


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[handlers])

    config = read_config()

    search_service = providers.Singleton(SearchService)