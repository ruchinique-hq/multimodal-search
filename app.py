from tornado.web import Application
from tornado.ioloop import IOLoop

from containers import Container

from handlers.search_handler import SearchHandler
from handlers.health_handler import HealthHandler

from services.search_service import SearchService


def initialise_handlers(search_service: SearchService):
    return [
        (r"/health", HealthHandler),
        (r"/search", SearchHandler, dict(search_service=search_service))
    ]

if __name__ == "__main__":
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__, "handlers"])

    handlers_list = initialise_handlers(
        search_service=container.search_service()
    )

    port = container.config.server.port() or 8080

    app = Application(handlers=handlers_list)
    app.container = container
    app.listen(port)

    print('started tornado application')

    IOLoop.current().start()