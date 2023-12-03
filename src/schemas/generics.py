from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

AnySch = TypeVar("AnySch")


class ResponseAsList(BaseModel, Generic[AnySch]):
    data: list[AnySch]
    count: Optional[int] | None = None
