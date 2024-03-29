from datetime import datetime
from typing import Optional, TypedDict

from pydantic import BaseModel, ConfigDict


class ProjectBase(BaseModel):
    name: str
    image: str
    url: str
    description: str
    tags: list[str]
    post_id: Optional[int] = None
    coming_soon: Optional[bool] = False


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    name: Optional[str] = None
    image: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[list[str]] = None
    coming_soon: Optional[bool] = None


class Project(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class QuerySchema(TypedDict, total=False):
    id: int
    name: str
    coming_soon: bool
