from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import quote_plus

ROOT_DIR = Path(__file__).resolve().parent.parent
DATASET_FILE = ROOT_DIR / "database" / "dataset" / "ecommerce_sales_analytics_5000.csv"
SCHEMA_DIR = ROOT_DIR / "database" / "schema"
ENV_FILE = ROOT_DIR / ".env"


def load_env_file(path: Path) -> None:
    """Load KEY=VALUE pairs from a .env file without overriding real env vars."""
    if not path.is_file():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            os.environ.setdefault(key, value)


def dsn_from_env() -> str:
    """Build a DSN from DATABASE_URL or the individual DB_* settings."""
    database_url = os.environ.get("DATABASE_URL", "")
    if database_url:
        return database_url

    if not (os.environ.get("DB_NAME") or os.environ.get("DB_USER")):
        return ""  # fall back to libpq defaults

    user = quote_plus(os.environ.get("DB_USER", "postgres"))
    password = os.environ.get("DB_PASSWORD", "")
    auth = f"{user}:{quote_plus(password)}" if password else user
    host = os.environ.get("DB_HOST", "localhost")
    port = os.environ.get("DB_PORT", "5432")
    name = os.environ.get("DB_NAME", "")
    return f"postgresql://{auth}@{host}:{port}/{name}"
