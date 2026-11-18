from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import psycopg  # noqa: E402

from config import (  # noqa: E402
    DATASET_FILE,
    ENV_FILE,
    dsn_from_env,
    load_env_file,
)
from database.etl.extract import ExtractError  # noqa: E402
from database.etl.pipeline import run_etl  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Load the e-commerce CSV into PostgreSQL.")
    parser.add_argument(
        "--csv",
        type=Path,
        default=DATASET_FILE,
        help=f"source CSV file (default: {DATASET_FILE})",
    )
    parser.add_argument(
        "--dsn",
        default=dsn_from_env(),
        help="PostgreSQL connection string (default: DATABASE_URL, DB_* from .env, or libpq defaults)",
    )
    return parser.parse_args()


def has_loaded_data(dsn: str) -> bool:
    """Return True when fact_orders already contains rows."""
    with psycopg.connect(dsn) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT EXISTS (SELECT 1 FROM fact_orders)")
            row = cur.fetchone()
            return bool(row and row[0])


def main() -> int:
    load_env_file(ENV_FILE)
    args = parse_args()

    if not args.csv.is_file():
        print(f"CSV not found: {args.csv}", file=sys.stderr)
        return 1

    print("Connecting to database")
    try:
        if has_loaded_data(args.dsn):
            print("fact_orders already has data; skipping ETL.")
            return 0
    except psycopg.errors.UndefinedTable:
        print(
            "fact_orders table not found. Run scripts/run_schema.py first.",
            file=sys.stderr,
        )
        return 1
    except psycopg.Error as exc:
        print(f"Connection failed: {exc}", file=sys.stderr)
        return 1

    try:
        stats = run_etl(args.csv, args.dsn)
    except ExtractError as exc:
        print(f"Extract failed: {exc}", file=sys.stderr)
        return 1
    except psycopg.Error as exc:
        print(f"Load failed: {exc}", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"ETL failed: {exc}", file=sys.stderr)
        return 1

    print(f"Extracted {stats.extracted} rows from {args.csv.name}")
    print(
        f"Loaded {stats.customers} customers, "
        f"{stats.product_categories} product categories, "
        f"{stats.regions} regions, "
        f"{stats.payments} payment methods, "
        f"{stats.orders} orders."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
