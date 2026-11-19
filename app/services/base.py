from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Generic, TypeVar

from sqlalchemy.orm import Session

from app.models.base import Base
from app.repositories.base import ReadRepository

ModelT = TypeVar("ModelT", bound=Base)


@dataclass(frozen=True)
class Page(Generic[ModelT]):
    """One page of rows plus backend-computed pagination metadata."""

    items: Sequence[ModelT]
    page: int
    page_size: int
    total: int

    @property
    def total_pages(self) -> int:
        return (self.total + self.page_size - 1) // self.page_size

    @property
    def has_next(self) -> bool:
        return self.page < self.total_pages

    @property
    def has_previous(self) -> bool:
        return self.page > 1


class ReadService(Generic[ModelT]):
    """Read operations delegated to a repository."""

    def __init__(self, repository: ReadRepository[ModelT]) -> None:
        self.repository = repository

    def list(self, session: Session, *, limit: int, offset: int) -> Sequence[ModelT]:
        return self.repository.list(session, limit=limit, offset=offset)

    def get(self, session: Session, item_id: int) -> ModelT | None:
        return self.repository.get(session, item_id)

    def paginate(self, session: Session, *, page: int, page_size: int) -> Page[ModelT]:
        offset = (page - 1) * page_size
        items = self.repository.list(session, limit=page_size, offset=offset)
        total = self.repository.count(session)
        return Page(items=items, page=page, page_size=page_size, total=total)
