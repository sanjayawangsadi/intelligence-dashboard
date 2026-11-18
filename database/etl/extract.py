from __future__ import annotations

import csv
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

from database.etl.models import RawOrder

DATE_FORMAT = "%m/%d/%Y"
REQUIRED_COLUMNS = (
    "order_id",
    "order_date",
    "customer_id",
    "product_category",
    "region",
    "quantity",
    "unit_price",
    "discount",
    "payment_method",
    "delivery_days",
    "customer_rating",
    "revenue",
)


class ExtractError(ValueError):
    """Raised when the source CSV is missing columns or has an invalid value."""


def _parse_int(row: dict[str, str], column: str, line: int) -> int:
    try:
        return int(row[column].strip())
    except (TypeError, ValueError) as exc:
        raise ExtractError(f"line {line}: invalid {column}={row[column]!r}") from exc


def _parse_decimal(row: dict[str, str], column: str, line: int) -> Decimal:
    try:
        return Decimal(row[column].strip())
    except (TypeError, InvalidOperation) as exc:
        raise ExtractError(f"line {line}: invalid {column}={row[column]!r}") from exc


def _parse_text(row: dict[str, str], column: str, line: int) -> str:
    value = (row[column] or "").strip()
    if not value:
        raise ExtractError(f"line {line}: empty {column}")
    return value


def _parse_date(row: dict[str, str], column: str, line: int) -> date:
    value = _parse_text(row, column, line)
    try:
        return datetime.strptime(value, DATE_FORMAT).date()
    except ValueError as exc:
        raise ExtractError(
            f"line {line}: invalid {column}={value!r}, expected {DATE_FORMAT}"
        ) from exc


def read_orders(path: Path) -> list[RawOrder]:
    """Read and validate the source CSV into typed rows."""
    rows: list[RawOrder] = []

    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        missing = [column for column in REQUIRED_COLUMNS if column not in (reader.fieldnames or [])]
        if missing:
            raise ExtractError(f"{path}: missing columns: {', '.join(missing)}")

        for line, row in enumerate(reader, start=2):
            rows.append(
                RawOrder(
                    order_id=_parse_int(row, "order_id", line),
                    order_date=_parse_date(row, "order_date", line),
                    customer_id=_parse_int(row, "customer_id", line),
                    product_category=_parse_text(row, "product_category", line),
                    region=_parse_text(row, "region", line),
                    quantity=_parse_int(row, "quantity", line),
                    unit_price=_parse_decimal(row, "unit_price", line),
                    discount=_parse_decimal(row, "discount", line),
                    payment_method=_parse_text(row, "payment_method", line),
                    delivery_days=_parse_int(row, "delivery_days", line),
                    customer_rating=_parse_decimal(row, "customer_rating", line),
                    revenue=_parse_decimal(row, "revenue", line),
                )
            )

    return rows
