from app.models import DimProductCategory
from app.repositories.dim_product_category_repository import (
    DimProductCategoryRepository,
)
from app.services.base import ReadService


class DimProductCategoryService(ReadService[DimProductCategory]):
    def __init__(self) -> None:
        super().__init__(DimProductCategoryRepository())
