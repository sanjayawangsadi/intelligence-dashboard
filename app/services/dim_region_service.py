from app.models import DimRegion
from app.repositories.dim_region_repository import DimRegionRepository
from app.services.base import ReadService


class DimRegionService(ReadService[DimRegion]):
    def __init__(self) -> None:
        super().__init__(DimRegionRepository())
