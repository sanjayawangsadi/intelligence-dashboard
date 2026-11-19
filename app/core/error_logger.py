from __future__ import annotations

import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


async def log_unhandled_exception(request: Request, exc: Exception) -> JSONResponse:
    """Log the traceback and return a generic 500 response."""
    logger.error(
        "Unhandled error: %s %s",
        request.method,
        request.url.path,
        exc_info=(type(exc), exc, exc.__traceback__),
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error."},
    )


def register_error_logger(app: FastAPI) -> None:
    """Attach the unhandled-exception logger to the application."""
    app.add_exception_handler(Exception, log_unhandled_exception)
