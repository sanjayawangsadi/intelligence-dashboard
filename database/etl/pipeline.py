from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import psycopg

from database.etl.extract import read_orders
from database.etl.load import load
from database.etl.transform import transform


@dataclass(frozen=True)
class EtlStats:
    extracted: int
    customers: int
    product_categories: int
    regions: int
    payments: int
    orders: int


def run_etl(csv_path: Path, dsn: str = "") -> EtlStats:
    """Extract the CSV, transform it, and upsert it into PostgreSQL."""
    raw_orders = read_orders(csv_path)
    if not raw_orders:
        raise ValueError(f"{csv_path}: no data rows found")

    data = transform(raw_orders)

    with psycopg.connect(dsn) as conn:
        load(conn, data)

    return EtlStats(
        extracted=len(raw_orders),
        customers=len(data.customers),
        product_categories=len(data.product_categories),
        regions=len(data.regions),
        payments=len(data.payments),
        orders=len(data.orders),
    )
