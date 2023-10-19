from datetime import datetime
from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from src.database.base import Base


class Asset(Base):
    __tablename__ = "asset"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    key: Mapped[str] = mapped_column(unique=True)
    mimetype: Mapped[str]
    created_at: Mapped[Optional[datetime]] = mapped_column(insert_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        insert_default=func.now(), onupdate=func.now()
    )
