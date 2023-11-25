import enum
from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.dialects.postgresql import ARRAY, ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base


class Status(enum.Enum):
    editing = "editing"
    active = "active"
    inactive = "inactive"


class Project(Base):
    __tablename__ = "project"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[str]
    image: Mapped[str]
    url: Mapped[str]
    description: Mapped[str] = mapped_column(String(240))
    tags: Mapped[Optional[list[str]]] = mapped_column(ARRAY(String))
    status: Mapped[Status] = mapped_column(ENUM(Status, name="status"))
    coming_soon: Mapped[bool] = mapped_column(default=False, nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(insert_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        insert_default=func.now(), onupdate=func.now()
    )
    post_id: Mapped[Optional[int]] = mapped_column(ForeignKey("post.id"))
    post: Mapped[Optional["Post"]] = relationship(back_populates="project")  # noqa
