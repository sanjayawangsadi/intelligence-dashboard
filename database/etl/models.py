from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(frozen=True)
class RawOrder:
    """One row of the source CSV, parsed and typed."""

    order_id: int
    order_date: date
    customer_id: int
    product_category: str
    region: str
    quantity: int
    unit_price: Decimal
    discount: Decimal
    payment_method: str
    delivery_days: int
    customer_rating: Decimal
    revenue: Decimal


@dataclass(frozen=True)
class Customer:
    id: int
    customer_unique_id: int


@dataclass(frozen=True)
class Dimension:
    id: int
    name: str


@dataclass(frozen=True)
class FactOrder:
    id: int
    order_id: int
    order_date: date
    customer_id: int
    product_category_id: int
    region_id: int
    quantity: int
    unit_price: Decimal
    discount: Decimal
    payment_id: int
    delivery_days: int
    customer_rating: int
    revenue: Decimal


@dataclass(frozen=True)
class TransformedData:
    customers: list[Customer]
    product_categories: list[Dimension]
    regions: list[Dimension]
    payments: list[Dimension]
    orders: list[FactOrder]
