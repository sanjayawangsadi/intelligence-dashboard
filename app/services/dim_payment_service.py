from app.models import DimPayment
from app.repositories.dim_payment_repository import DimPaymentRepository
from app.services.base import ReadService


class DimPaymentService(ReadService[DimPayment]):
    def __init__(self) -> None:
        super().__init__(DimPaymentRepository())
