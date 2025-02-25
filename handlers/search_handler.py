import json

from tornado import gen, web
from dependency_injector.wiring import inject

from handlers.base_handler import BaseHandler

from models.requests.search import GetAnswerRequest

from services.search_service import SearchService

from logger import logger


class SearchHandler(BaseHandler):
    search_service: SearchService

    def initialize(self, search_service: SearchService):
        self.search_service = search_service

    @inject
    @gen.coroutine
    def post(self):
        try:
            logger.debug(f"received request to get answer: {self.request.body}")
            
            body = self.request.body.decode('utf-8')
            
            if not body:
                self.send_error_response(400, 'please provide a valid query request')
                return

            body_json = json.loads(body)
            request = GetAnswerRequest(**body_json)
            response = self.search_service.generate_answer(request)

            logger.info(f"processed request for query: {request.question}")
            
            if response:
                self.write(response.model_dump())
            else:
                self.send_error_response(500, 'failed to generate answer')
            
        except json.JSONDecodeError:
            self.send_error_response(400, 'invalid json in request body')
        except Exception as err:
            self.send_error_response(500, f'failed to generate answer: {err.__str__()}')
        finally:
            self.finish()
