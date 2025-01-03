import json

from tornado import gen, web
from dependency_injector.wiring import inject

from handlers.base_handler import BaseHandler

from services.search_service import SearchService
from models.requests.search import SearchAnswerRequest
from models.responses.answer import SearchAnswerResponse

from logger import logger


class SearchHandler(BaseHandler):
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
            logger.info(f"received a request to generate answer for query {search_answer_request.query}")

            response: SearchAnswerResponse = self.search_service.generate_answer(search_answer_request)
            if response is None:
                self.set_status(400)
                self.write({'message': f'failed to generate answer for query {search_answer_request.query}'})
            else:
                self.set_status(200)
                self.write(json.dumps(response.to_json()))

        except Exception as err:
            self.set_status(400)
            self.write({'message': f'failed to generate answer for query {search_answer_request.query} {err.__str__()}'})
        finally:
            self.finish()
