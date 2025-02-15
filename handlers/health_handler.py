from dependency_injector.wiring import inject
from tornado import gen, web

class HealthHandler(web.RequestHandler):

    @inject
    @gen.coroutine
    def get(self):
        self.write({'message': 'Multimodal Search API is Running'})