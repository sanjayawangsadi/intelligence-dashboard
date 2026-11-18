from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal

from database.etl.models import (
    Customer,
    Dimension,
    FactOrder,
    RawOrder,
    TransformedData,
)


def _dimension_values(raw_orders: list[RawOrder], attribute: str) -> list[Dimension]:
    """Assign stable ids from sorted distinct names."""
    names = sorted({getattr(row, attribute) for row in raw_orders})
    return [Dimension(id=index, name=name) for index, name in enumerate(names, start=1)]


def _rating_as_smallint(rating: Decimal, order_id: int) -> int:
    value = int(rating.quantize(Decimal("1"), rounding=ROUND_HALF_UP))
    if not 1 <= value <= 5:
        raise ValueError(f"order {order_id}: customer_rating {rating} outside 1..5")
    return value


def transform(raw_orders: list[RawOrder]) -> TransformedData:
    """Build dimension and fact rows from the extracted orders."""
    customers = [
        Customer(id=customer_id, customer_unique_id=customer_id)
        for customer_id in sorted({row.customer_id for row in raw_orders})
    ]
    product_categories = _dimension_values(raw_orders, "product_category")
    regions = _dimension_values(raw_orders, "region")
    payments = _dimension_values(raw_orders, "payment_method")

    category_ids = {dimension.name: dimension.id for dimension in product_categories}
    region_ids = {dimension.name: dimension.id for dimension in regions}
    payment_ids = {dimension.name: dimension.id for dimension in payments}

    orders = [
        FactOrder(
            id=row.order_id,
            order_id=row.order_id,
            order_date=row.order_date,
            customer_id=row.customer_id,
            product_category_id=category_ids[row.product_category],
            region_id=region_ids[row.region],
            quantity=row.quantity,
            unit_price=row.unit_price,
            discount=row.discount,
            payment_id=payment_ids[row.payment_method],
            delivery_days=row.delivery_days,
            customer_rating=_rating_as_smallint(row.customer_rating, row.order_id),
            revenue=row.revenue,
        )
        for row in raw_orders
    ]

    return TransformedData(
        customers=customers,
        product_categories=product_categories,
        regions=regions,
        payments=payments,
        orders=orders,
    )
