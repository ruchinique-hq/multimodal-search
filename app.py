from tornado.web import Application
from tornado.ioloop import IOLoop

from containers import Container

from handlers.health_handler import HealthHandler
from handlers.file_handler import FileHandler
from handlers.search_handler import SearchHandler

from services.amazon_service import AmazonService
from services.search_service import SearchService

from logger import logger


def initialise_handlers(amazon_service: AmazonService, search_service: SearchService):
    return [
        (r"/health", HealthHandler),
        (r"/file", FileHandler, dict(amazon_service=amazon_service)),
        (r"/search", SearchHandler, dict(search_service=search_service))
    ]

if __name__ == "__main__":
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__, "handlers"])

    handlers_list = initialise_handlers(
        amazon_service=container.amazon_service(), 
        search_service=container.search_service()
    )

    port = container.config.server.port() or 8080

    app = Application(handlers=handlers_list)
    app.container = container
    app.listen(port)

    logger.info("application started successfully")
    IOLoop.current().start()