from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from config.database import get_session
from app.models import DimProductCategory
from app.dtos.dim_product_category import DimProductCategoryDTO
from app.dtos.pagination import PageDTO
from app.services.dim_product_category_service import DimProductCategoryService

router = APIRouter(prefix="/product-categories", tags=["product-categories"])
service = DimProductCategoryService()


@router.get(
    "",
    response_model=PageDTO[DimProductCategoryDTO],
    summary="List product categories",
    description="Return product categories ordered by primary key.",
    response_description="A page of product categories.",
)
def list_product_categories(
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
    "/{category_id}",
    response_model=DimProductCategoryDTO,
    summary="Get one product category",
    description="Fetch a single product category by primary key.",
    response_description="The requested product category.",
    responses={404: {"description": "Product category not found."}},
)
def get_product_category(
    category_id: int,
    session: Session = Depends(get_session),
) -> DimProductCategory:
    category = service.get(session, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Product category not found.")
    return category
