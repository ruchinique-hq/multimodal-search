import json

from tornado import gen, web
from dependency_injector.wiring import inject

from handlers.base_handler import BaseHandler
from services.amazon_service import AmazonService

from models.requests.file import CreatePreSignedUrlRequest

from logger import logger


class FileHandler(BaseHandler):
    amazon_service: AmazonService

    def initialize(self, amazon_service: AmazonService):
        self.amazon_service = amazon_service

    @inject
    @gen.coroutine
    def post(self):
        try:
            body = self.request.body
            body = body.decode('utf-8')

            if body is None or body == "":
                self.set_status(400)
                self.write({'message': 'please provide valid details to generate pre-signed url'})
                self.finish()

            body_json = json.loads(body)

            request = CreatePreSignedUrlRequest(**body_json)
            response: dict | None = self.amazon_service.generate_pre_signed_url(request)
            if response is None:
                logger.warn(f"failed to generate pre-signed url")
                self.set_status(400)
                self.write({'message': f'failed to generate pre-signed url'})
            else:
                logger.info(f"generated pre-signed url successfully")
                self.set_status(200)
                self.write(json.dumps(response))

        except Exception as err:
            self.set_status(400)
            self.write({'message': f'failed to generate answer for {err.__str__()}'})
        finally:
            self.finish()                    
    