import json

from tornado import gen, web
from dependency_injector.wiring import inject

from services.search_service import SearchService
from models.requests.search import SearchAnswerRequest


class SearchHandler(web.RequestHandler):
    search_service: SearchService

    def initialize(self, search_service: SearchService):
        self.search_service = search_service

    @inject
    @gen.coroutine
    def post(self):
        try:
            body = self.request.body
            body = body.decode('utf-8')

            if body is None or body == "":
                self.set_status(400)
                self.write({'message': 'please provide a valid query request'})
                self.finish()

            search_answer_request = SearchAnswerRequest(body)
            response = self.search_service.generate_answer(search_answer_request)

            self.set_status(200)
            self.write(json.dumps(response.to_json()))

        except Exception as err:
            self.set_status(400)
            self.write({'message': f'failed to get an answer for query {err.__str__()}'})
        finally:
            self.finish()
