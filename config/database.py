from __future__ import annotations

from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from config.settings import ENV_FILE, dsn_from_env, load_env_file

load_env_file(ENV_FILE)


def _sqlalchemy_dsn() -> str:
    """Return a SQLAlchemy DSN that uses the installed psycopg driver."""
    dsn = dsn_from_env()
    if not dsn:
        return "postgresql+psycopg://"
    for prefix in ("postgresql://", "postgres://"):
        if dsn.startswith(prefix):
            return f"postgresql+psycopg://{dsn[len(prefix):]}"
    return dsn


engine = create_engine(_sqlalchemy_dsn(), pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_session() -> Iterator[Session]:
    """Yield one session per request."""
    with SessionLocal() as session:
        yield session
