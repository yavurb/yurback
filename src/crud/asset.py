from src.crud.base import CRUDBase
from src.models.asset import Asset
from src.schemas.asset import Asset as AssetSchema
from src.schemas.asset import CreateAsset, QuerySchema, UpdateAsset


class CRUDAsset(
    CRUDBase[
        Asset,
        AssetSchema,
        CreateAsset,
        UpdateAsset,
        QuerySchema,
    ]
):
    pass


asset = CRUDAsset(Asset, AssetSchema)
