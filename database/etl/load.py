from __future__ import annotations

import psycopg

from database.etl.models import TransformedData

CUSTOMER_SQL = """
INSERT INTO dim_customers (id, customer_unique_id)
VALUES (%s, %s)
ON CONFLICT (id) DO UPDATE
SET customer_unique_id = EXCLUDED.customer_unique_id
"""

DIMENSION_SQL = """
INSERT INTO dim_{table} (id, {column})
VALUES (%s, %s)
ON CONFLICT (id) DO UPDATE
SET {column} = EXCLUDED.{column}
"""

FACT_SQL = """
INSERT INTO fact_orders (
    id,
    order_id,
    order_date,
    customer_id,
    product_category_id,
    region_id,
    quantity,
    unit_price,
    discount,
    payment_id,
    delivery_days,
    customer_rating,
    revenue
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (id) DO UPDATE
SET order_id            = EXCLUDED.order_id,
    order_date          = EXCLUDED.order_date,
    customer_id         = EXCLUDED.customer_id,
    product_category_id = EXCLUDED.product_category_id,
    region_id           = EXCLUDED.region_id,
    quantity            = EXCLUDED.quantity,
    unit_price          = EXCLUDED.unit_price,
    discount            = EXCLUDED.discount,
    payment_id          = EXCLUDED.payment_id,
    delivery_days       = EXCLUDED.delivery_days,
    customer_rating     = EXCLUDED.customer_rating,
    revenue             = EXCLUDED.revenue
"""


def load(conn: psycopg.Connection, data: TransformedData) -> None:
    """Upsert dimensions first, then facts, inside the caller's transaction."""
    with conn.cursor() as cur:
        cur.executemany(
            CUSTOMER_SQL,
            [(customer.id, customer.customer_unique_id) for customer in data.customers],
        )
        for table, column, dimensions in (
            ("product_categories", "product_category", data.product_categories),
            ("regions", "region", data.regions),
            ("payments", "payment", data.payments),
        ):
            cur.executemany(
                DIMENSION_SQL.format(table=table, column=column),
                [(dimension.id, dimension.name) for dimension in dimensions],
            )
        cur.executemany(
            FACT_SQL,
            [
                (
                    order.id,
                    order.order_id,
                    order.order_date,
                    order.customer_id,
                    order.product_category_id,
                    order.region_id,
                    order.quantity,
                    order.unit_price,
                    order.discount,
                    order.payment_id,
                    order.delivery_days,
                    order.customer_rating,
                    order.revenue,
                )
                for order in data.orders
            ],
        )
