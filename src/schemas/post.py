from datetime import datetime
from typing import Optional, TypedDict

from pydantic import BaseModel, ConfigDict

from src.models.post import Status


class PostBase(BaseModel):
    title: str
    author: str
    slug: str
    status: Status = Status.published
    description: str
    content: str


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    title: Optional[str] = None
    author: Optional[str] = None
    slug: Optional[str] = None
    status: Optional[Status] = None
    description: Optional[str] = None
    content: Optional[str] = None
    published_at: Optional[datetime] = None


class Post(PostBase):
    id: int
    created_at: datetime
    updated_at: datetime
    published_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


class QuerySchema(TypedDict, total=False):
    id: int
    title: str
    author: str
    slug: str
    status: Status
