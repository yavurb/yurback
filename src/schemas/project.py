from datetime import datetime
from typing import Optional, TypedDict

from pydantic import BaseModel, ConfigDict

from src.models.project import Status


class ProjectBase(BaseModel):
    name: str
    status: Status = Status.editing
    image: str
    url: str
    description: str
    tags: list[str]
    post_id: Optional[int] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    name: Optional[str] = None
    status: Optional[Status] = None
    image: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[list[str]] = None


class Project(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class QuerySchema(TypedDict, total=False):
    id: int
    name: str
    status: Status
