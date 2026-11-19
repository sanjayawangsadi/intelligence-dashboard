from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from config.database import get_session
from app.models import DimRegion
from app.dtos.dim_region import DimRegionDTO
from app.dtos.pagination import PageDTO
from app.services.dim_region_service import DimRegionService

router = APIRouter(prefix="/regions", tags=["regions"])
service = DimRegionService()


@router.get(
    "",
    response_model=PageDTO[DimRegionDTO],
    summary="List regions",
    description="Return regions ordered by primary key.",
    response_description="A page of regions.",
)
def list_regions(
    page: int = Query(
        default=1,
        ge=1,
        description="Page number to return (1-based).",
    ),
    page_size: int = Query(
        default=100,
        ge=1,
        le=500,
        description="Maximum rows per page.",
    ),
    session: Session = Depends(get_session),
) -> dict[str, object]:
    result = service.paginate(session, page=page, page_size=page_size)
    return {
        "items": result.items,
        "page": result.page,
        "page_size": result.page_size,
        "total": result.total,
        "total_pages": result.total_pages,
        "has_next": result.has_next,
        "has_previous": result.has_previous,
    }


@router.get(
    "/{region_id}",
    response_model=DimRegionDTO,
    summary="Get one region",
    description="Fetch a single region by primary key.",
    response_description="The requested region.",
    responses={404: {"description": "Region not found."}},
)
def get_region(
    region_id: int,
    session: Session = Depends(get_session),
) -> DimRegion:
    region = service.get(session, region_id)
    if region is None:
        raise HTTPException(status_code=404, detail="Region not found.")
    return region
