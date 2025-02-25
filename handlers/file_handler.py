import json
from tornado import gen
from dependency_injector.wiring import inject
from handlers.base_handler import BaseHandler
from services.amazon_service import AmazonService
from services.asset_service import AssetService
from models.requests.file import CreateSignedUrlRequest, ProcessFileRequest
from logger import logger

class FileHandler(BaseHandler):
    def initialize(self, asset_service: AssetService, amazon_service: AmazonService):
        self.asset_service = asset_service
        self.amazon_service = amazon_service

    @inject
    @gen.coroutine
    def post(self, path):
        try:
            logger.debug(f"received request to process file for {path}: {self.request.body}")
            body = json.loads(self.request.body.decode('utf-8'))

            if not body:
                self.send_error_response(400, 'please provide valid details')
                return

            if path == 'initialize':
                yield self.generate_pre_signed_url(CreateSignedUrlRequest(**body))
            elif path == 'process':
                yield self.process_file(ProcessFileRequest(**body))
            else:
                self.send_error_response(400, 'invalid path')
                return

            logger.debug("processed file request successfully")

        except json.JSONDecodeError:
            self.send_error_response(400, 'invalid json in request body')
        except Exception as err:
            self.send_error_response(400, f'failed to process request: {str(err)}')
        finally:
            self.finish()

    def generate_pre_signed_url(self, request: CreateSignedUrlRequest):
        response = self.amazon_service.generate_pre_signed_url(request)
        if response is None:
            logger.warn("failed to generate pre-signed url")
            self.send_error_response(400, 'failed to generate pre-signed url')
        else:
            logger.info("generated pre-signed url successfully")
            self.write(json.dumps(response))

    def process_file(self, request: ProcessFileRequest):
        s3_content = self.amazon_service.get_object(request.key)
        if not s3_content:
            self.send_error_response(500, 'failed to get object from s3')
            return

        asset_id = self.asset_service.create_asset(request.fingerprint, s3_content)
        if not asset_id:
            self.send_error_response(500, 'failed to create asset')
            return
        
        self.asset_service.trigger_processing(asset_id)        
        self.write({'message': 'triggered file for processing'})