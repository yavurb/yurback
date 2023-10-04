from datetime import datetime

from pydantic import BaseModel, ConfigDict

from models.post import Status


class PostBase(BaseModel):
    title: str
    author: str
    slug: str
    status: Status = Status.editing
    description: str
    content: str


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    published_at: datetime


class Post(PostBase):
    id: int
    created_at: datetime
    updated_at: datetime
    published_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
