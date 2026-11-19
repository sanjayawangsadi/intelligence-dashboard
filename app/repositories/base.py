from __future__ import annotations

from collections.abc import Sequence
from typing import Generic, TypeVar

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.base import Base

ModelT = TypeVar("ModelT", bound=Base)


class ReadRepository(Generic[ModelT]):
    """Shared read-only queries for the DWH tables."""

    def __init__(self, model: type[ModelT]) -> None:
        self.model = model

    def list(self, session: Session, *, limit: int, offset: int) -> Sequence[ModelT]:
        stmt = (
            select(self.model)
            .order_by(self.model.id)  # type: ignore[attr-defined]
            .limit(limit)
            .offset(offset)
        )
        return session.scalars(stmt).all()

    def get(self, session: Session, item_id: int) -> ModelT | None:
        return session.get(self.model, item_id)

    def count(self, session: Session) -> int:
        stmt = select(func.count()).select_from(self.model)
        return session.scalar(stmt) or 0
