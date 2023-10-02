import enum
import uuid
from typing import Optional
from sqlalchemy import String, Text, DateTime, Enum, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

from database.base import Base


class Status(enum.Enum):
    editing = "editing"
    active = "active"
    inactive = "inactive"


class Post(Base):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    title: Mapped[str] = mapped_column(String(60))
    author: Mapped[str]
    slug: Mapped[str]
    status: Mapped[Status] = mapped_column(Enum(Status))
    description: Mapped[str]
    content: Mapped[str] = mapped_column(Text())
    created_at: Mapped[Optional[datetime]] = mapped_column(insert_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        insert_default=func.now(), onupdate=func.now()
    )
    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime())
