from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from config import ENV_FILE, SCHEMA_DIR, dsn_from_env, load_env_file  # noqa: E402

RUNNER_FILE = "run_all.sql"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dsn",
        default=dsn_from_env(),
        help="PostgreSQL connection string (default: DATABASE_URL, DB_* from .env, or libpq defaults)",
    )
    return parser.parse_args()


def sql_files() -> list[Path]:
    return [
        path
        for path in sorted(SCHEMA_DIR.glob("*.sql"))
        if path.name != RUNNER_FILE
    ]


def main() -> int:
    load_env_file(ENV_FILE)

    try:
        import psycopg
    except ImportError:
        print(
            "psycopg is not installed. Run with:\n"
            "  uv run --with 'psycopg[binary]' python scripts/run_schema.py",
            file=sys.stderr,
        )
        return 1

    args = parse_args()
    files = sql_files()

    if not files:
        print(f"No SQL files found in {SCHEMA_DIR}", file=sys.stderr)
        return 1

    print(f"Connecting to database")
    try:
        conn = psycopg.connect(args.dsn, autocommit=True)
    except psycopg.Error as exc:
        print(f"Connection failed: {exc}", file=sys.stderr)
        return 1

    failed = False
    try:
        for path in files:
            print(f"Applying {path.name} ... ", end="", flush=True)
            try:
                with conn.cursor() as cur:
                    cur.execute(path.read_text(encoding="utf-8"))
            except psycopg.Error as exc:
                print("FAILED")
                print(f"{path.name}: {exc}", file=sys.stderr)
                conn.rollback()
                failed = True
                break
            print("OK")
    finally:
        conn.close()

    if failed:
        return 1

    print(f"Done: {len(files)} files applied.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
