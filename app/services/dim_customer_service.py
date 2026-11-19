from app.models import DimCustomer
from app.repositories.dim_customer_repository import DimCustomerRepository
from app.services.base import ReadService


class DimCustomerService(ReadService[DimCustomer]):
    def __init__(self) -> None:
        super().__init__(DimCustomerRepository())
