from app.models import DimProductCategory
from app.repositories.base import ReadRepository


class DimProductCategoryRepository(ReadRepository[DimProductCategory]):
    def __init__(self) -> None:
        super().__init__(DimProductCategory)
