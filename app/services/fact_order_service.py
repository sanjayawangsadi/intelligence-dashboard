from __future__ import annotations

from sqlalchemy.orm import Session

from app.models import FactOrder
from app.repositories.fact_order_repository import FactOrderRepository
from app.services.base import ReadService


class FactOrderService(ReadService[FactOrder]):
    def __init__(self) -> None:
        super().__init__(FactOrderRepository())
        self.repository: FactOrderRepository

    def get_by_order_id(self, session: Session, order_id: int) -> FactOrder | None:
        return self.repository.get_by_order_id(session, order_id)
