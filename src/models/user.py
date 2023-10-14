from datetime import datetime
from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from src.database.base import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    username: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    created_at: Mapped[Optional[datetime]] = mapped_column(insert_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        insert_default=func.now(), onupdate=func.now()
    )
