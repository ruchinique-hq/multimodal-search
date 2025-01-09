from models.asset import Asset
from repositories.asset_repositories import AssetRepository


class AssetService:
    def __init__(self, asset_repository: AssetRepository):
        self.asset_repository = asset_repository

    