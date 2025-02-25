from pydantic import BaseModel

from models.asset.asset import Asset

class SearchAssetResponse(BaseModel):
    id: str
    name: str
    
    def __init__(self, asset: Asset):
        self.id = str(asset.id)
        self.name = asset.name
        
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name
        }