from datetime import datetime
from typing import TypedDict

from pydantic import BaseModel, ConfigDict


class BaseAsset(BaseModel):
    key: str
    mimetype: str


class CreateAsset(BaseAsset):
    pass


class UpdateAsset(BaseAsset):
    pass


class Asset(BaseAsset):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class QuerySchema(TypedDict, total=False):
    id: int
    mimetype: str
