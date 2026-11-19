from __future__ import annotations

import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from config.settings import ENV_FILE, ROOT_DIR, load_env_file

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
LOG_FILE = ROOT_DIR / "logs" / "app.log"
LOG_MAX_BYTES = 5 * 1024 * 1024
LOG_BACKUP_COUNT = 3


def setup_logging() -> None:
    """Configure stdout and rotating-file logging (LOG_LEVEL, LOG_FILE env)."""
    load_env_file(ENV_FILE)
    level = os.environ.get("LOG_LEVEL", "INFO").upper()

    log_file = Path(os.environ.get("LOG_FILE", LOG_FILE))
    if not log_file.is_absolute():
        log_file = ROOT_DIR / log_file
    log_file.parent.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(LOG_FORMAT)
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    logging.basicConfig(
        level=level,
        handlers=[console, file_handler],
    )
    logging.getLogger("app").setLevel(level)
