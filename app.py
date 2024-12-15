from tornado.web import Application
from tornado.ioloop import IOLoop

from containers import Container
from handlers.search_handler import SearchHandler

def initialise_handlers():
    return [
        (r"/search", SearchHandler)
    ]

if __name__ == "__main__":
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__, "handlers"])

    handlers_list = initialise_handlers()

    port = container.config.server.port() or 8080

    app = Application(handlers=handlers_list)
    app.container = container
    app.listen(port)

    print('started tornado application')

    IOLoop.current().start()