import tornado

class SearchHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, Tornado!")