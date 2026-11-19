from app.models import DimRegion
from app.repositories.base import ReadRepository


class DimRegionRepository(ReadRepository[DimRegion]):
    def __init__(self) -> None:
        super().__init__(DimRegion)
