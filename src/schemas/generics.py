from typing import Generic, TypeVar

from pydantic import BaseModel

AnySch = TypeVar("AnySch")


class ResponseAsList(BaseModel, Generic[AnySch]):
    data: list[AnySch]
