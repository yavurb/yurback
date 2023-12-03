import enum
from datetime import datetime
from typing import Literal, Optional

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base


class Status(enum.Enum):
    draft = "draft"
    published = "published"
    archived = "archived"


class Post(Base):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    title: Mapped[str] = mapped_column(String(60))
    author: Mapped[str]
    slug: Mapped[str] = mapped_column(unique=True)
    status: Mapped[Status] = mapped_column(ENUM(Status, name="status"))
    description: Mapped[str]
    content: Mapped[str] = mapped_column(Text())
    created_at: Mapped[Optional[datetime]] = mapped_column(insert_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        insert_default=func.now(), onupdate=func.now()
    )
    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime())
    project: Mapped[Optional[Literal["Project"]]] = relationship(
        back_populates="post"
    )  # noqa
