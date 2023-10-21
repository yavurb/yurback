from src.crud.base import CRUDBase
from src.models.asset import Asset
from src.schemas.asset import CreateAsset, QuerySchema, UpdateAsset


class CRUDAsset(CRUDBase[Asset, CreateAsset, UpdateAsset, QuerySchema]):
    pass


asset = CRUDAsset(Asset)
