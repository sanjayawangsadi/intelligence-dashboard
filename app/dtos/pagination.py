from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class PageDTO(BaseModel, Generic[T]):
    """Envelope for paginated collection responses."""

    items: list[T] = Field(description="Rows for the current page.")
    page: int = Field(description="Current page number (1-based).")
    page_size: int = Field(description="Maximum rows per page.")
    total: int = Field(description="Total rows across all pages.")
    total_pages: int = Field(description="Total number of pages.")
    has_next: bool = Field(description="Whether a next page exists.")
    has_previous: bool = Field(description="Whether a previous page exists.")
