import json

from tornado import gen, web
from dependency_injector.wiring import inject

from handlers.base_handler import BaseHandler
from services.amazon_service import AmazonService

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

            params = body_json['params']
            fingerprint = params['fingerprint']
            file_name = params['fileName']

            url = self.amazon_service.generate_pre_signed_url(fingerprint, file_name);
            if url is None:
                logger.warn(f"failed to generate pre-signed url")
                self.set_status(400)
                self.write({'message': f'failed to generate pre-signed url'})
            else:
                logger.info(f"generated pre-signed url successfully")
                self.set_status(200)
                self.write({'pre_signed_url': url })

        except Exception as err:
            self.set_status(400)
            self.write({'message': f'failed to generate answer for {err.__str__()}'})
        finally:
            self.finish()                    
    