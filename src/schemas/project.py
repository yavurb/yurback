from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from src.models.project import Status


class ProjectBase(BaseModel):
    name: str
    status: Status = Status.editing
    image: str
    url: str
    description: str
    tags: list[str]
    post_id: int


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    name: Optional[str] = None
    status: Optional[Status] = None
    image: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[list[str]] = None
    post_id: Optional[int] = None


class Project(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
