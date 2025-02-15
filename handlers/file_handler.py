import json

from tornado import gen, web
from dependency_injector.wiring import inject

from handlers.base_handler import BaseHandler

from services.amazon_service import AmazonService
from services.asset_service import AssetService

from models.requests.file import CreatePreSignedUrlRequest, ProcessingRequest

from logger import logger

S3_METADATA_KEYS = ['ContentLength', 'ContentType', 'LastModified', 'Metadata', 'ETag']


class FileHandler(BaseHandler):
    asset_service: AssetService
    amazon_service: AmazonService

    def initialize(self, asset_service: AssetService, amazon_service: AmazonService):
        self.asset_service = asset_service
        self.amazon_service = amazon_service

    @inject
    @gen.coroutine
    def post(self, path):
        try:

            logger.debug(f"received a request to process file {self.request.body} for {path}")

            body = self.request.body
            body = body.decode('utf-8')

            if body is None or body == "":
                self.send_error_response(400, 'please provide valid details to generate pre-signed url')
                self.finish()

            body_json = json.loads(body)

            if path == 'initialize':
                request = CreatePreSignedUrlRequest(**body_json)
                yield self.generate_pre_signed_url(request)
            elif path == 'process':
                request = ProcessingRequest(**body_json)
                yield self.process_file(request)

            logger.debug(f"processed file request successfully")

        except Exception as err:
            self.set_status(400)
            self.write({'message': f'failed to generate answer for {err.__str__()}'})
        finally:
            self.finish()

    def generate_pre_signed_url(self, request: CreatePreSignedUrlRequest):
        response = self.amazon_service.generate_pre_signed_url(request)
        if response is None:
            logger.warn(f"failed to generate pre-signed url")
            self.set_status(400)
            self.write({'message': f'failed to generate pre-signed url'})
        else:
            logger.info(f"generated pre-signed url successfully")
            self.set_status(200)
            self.write(json.dumps(response))

    def process_file(self, request: ProcessingRequest) -> None:
        s3_content = self.amazon_service.get_object(request.key)
        if not s3_content:
            self.send_error_response(500, 'failed to get object from s3')
            return

        asset_id: str = self.asset_service.create_asset(request.fingerprint, s3_content)
        if not asset_id:
            self.send_error_response(500, 'failed to create asset')
            return
        
        self.asset_service.trigger_processing(asset_id)        

        self.set_status(200)
        self.write({'message': f'triggered file for processing'})