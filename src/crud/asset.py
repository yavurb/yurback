from src.crud.base import CRUDBase
from src.models.asset import Asset
from src.schemas.asset import CreateAsset, UpdateAsset


class CRUDAsset(CRUDBase[Asset, CreateAsset, UpdateAsset]):
    pass


asset = CRUDAsset(Asset)
