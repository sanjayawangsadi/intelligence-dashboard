from app.models import DimPayment
from app.repositories.base import ReadRepository


class DimPaymentRepository(ReadRepository[DimPayment]):
    def __init__(self) -> None:
        super().__init__(DimPayment)
