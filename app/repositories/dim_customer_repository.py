from app.models import DimCustomer
from app.repositories.base import ReadRepository


class DimCustomerRepository(ReadRepository[DimCustomer]):
    def __init__(self) -> None:
        super().__init__(DimCustomer)
