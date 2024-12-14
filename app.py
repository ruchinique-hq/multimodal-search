import tornado.ioloop
import tornado.web

from handlers.search_handler import SearchHandler

def app():
    return tornado.web.Application([
        (r"/search", SearchHandler)
    ])

if __name__ == "__main__":
    app = app()
    app.listen(8888)

    tornado.ioloop.IOLoop.current().start()