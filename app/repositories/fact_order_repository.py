from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import FactOrder
from app.repositories.base import ReadRepository


class FactOrderRepository(ReadRepository[FactOrder]):
    def __init__(self) -> None:
        super().__init__(FactOrder)

    def get_by_order_id(self, session: Session, order_id: int) -> FactOrder | None:
        stmt = select(FactOrder).where(FactOrder.order_id == order_id)
        return session.scalars(stmt).one_or_none()
