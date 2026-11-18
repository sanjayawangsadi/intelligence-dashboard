from __future__ import annotations

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class DimCustomer(Base):
    __tablename__ = "dim_customers"
    __table_args__ = {"schema": "public"}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    customer_unique_id: Mapped[int | None] = mapped_column(BigInteger)
