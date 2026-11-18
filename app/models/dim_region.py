from __future__ import annotations

from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class DimRegion(Base):
    __tablename__ = "dim_regions"
    __table_args__ = {"schema": "public"}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    region: Mapped[str | None] = mapped_column(String(255))
