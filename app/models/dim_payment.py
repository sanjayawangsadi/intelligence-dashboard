from __future__ import annotations

from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class DimPayment(Base):
    __tablename__ = "dim_payments"
    __table_args__ = {"schema": "public"}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    payment: Mapped[str | None] = mapped_column(String(255))
