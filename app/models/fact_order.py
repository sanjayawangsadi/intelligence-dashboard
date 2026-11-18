from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import (
    BigInteger,
    Date,
    ForeignKey,
    Numeric,
    SmallInteger,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.dim_customer import DimCustomer
from app.models.dim_payment import DimPayment
from app.models.dim_product_category import DimProductCategory
from app.models.dim_region import DimRegion


class FactOrder(Base):
    __tablename__ = "fact_orders"
    __table_args__ = (
        UniqueConstraint("order_id", name="uq_fact_orders_order_id"),
        {"schema": "public"},
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    order_id: Mapped[int | None] = mapped_column(BigInteger)
    order_date: Mapped[date | None] = mapped_column(Date)
    customer_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "public.dim_customers.id", name="fk_fact_orders_customer"
        ),
        nullable=False,
    )
    product_category_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey(
            "public.dim_product_categories.id",
            name="fk_fact_orders_product_category",
        ),
    )
    region_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("public.dim_regions.id", name="fk_fact_orders_region"),
    )
    quantity: Mapped[int | None] = mapped_column()
    unit_price: Mapped[Decimal | None] = mapped_column(Numeric(12, 2))
    discount: Mapped[Decimal | None] = mapped_column(Numeric(5, 4))
    payment_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("public.dim_payments.id", name="fk_fact_orders_payment"),
    )
    delivery_days: Mapped[int | None] = mapped_column()
    customer_rating: Mapped[int | None] = mapped_column(SmallInteger)
    revenue: Mapped[Decimal | None] = mapped_column(Numeric(12, 2))

    customer: Mapped[DimCustomer] = relationship(foreign_keys=[customer_id])
    product_category: Mapped[DimProductCategory | None] = relationship(
        foreign_keys=[product_category_id]
    )
    region: Mapped[DimRegion | None] = relationship(foreign_keys=[region_id])
    payment: Mapped[DimPayment | None] = relationship(foreign_keys=[payment_id])
