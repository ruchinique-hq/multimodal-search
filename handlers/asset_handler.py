import json

from tornado import gen, web
from dependency_injector.wiring import inject

from handlers.base_handler import BaseHandler

from services.asset_service import AssetService

from models.asset.asset import Asset

from models.requests.asset import SearchAssetRequest
from models.responses.asset import SearchAssetResponse

from logger import logger

class AssetHandler(BaseHandler):
    asset_service: AssetService
    
    def initialize(self, asset_service: AssetService):
        self.asset_service = asset_service
        
    @inject
    @gen.coroutine    
    def get(self):
        try:
            logger.info(f"received a request to search assets {self.request.body}")
            
            body = self.request.body
            body = body.decode('utf-8')
            
            if body is None or body == "":
                self.set_status(400)
                self.write({'message': 'invalid search request'})
                self.finish()
                
            request = SearchAssetRequest(body)
    
            assets: list[Asset] = self.asset_service.fetch_all(request)
            if not assets:
                self.set_status(400)
                self.write({'message': 'failed to fetch assets'})
                
            response = [SearchAssetResponse(asset) for asset in assets]

            self.set_status(200)
            self.write(json.dumps([item.to_json for item in response]))
            
        except Exception as e:
            self.set_status(500)
            self.write({'message': f'failed to fetch assets {e.__str__()}'})
        finally:
            self.finish()