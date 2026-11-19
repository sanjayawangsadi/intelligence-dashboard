from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from config.database import get_session
from app.models import DimCustomer
from app.dtos.dim_customer import DimCustomerDTO
from app.dtos.pagination import PageDTO
from app.services.dim_customer_service import DimCustomerService

router = APIRouter(prefix="/customers", tags=["customers"])
service = DimCustomerService()


@router.get(
    "",
    response_model=PageDTO[DimCustomerDTO],
    summary="List customers",
    description="Return customers ordered by primary key.",
    response_description="A page of customers.",
)
def list_customers(
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
    "/{customer_id}",
    response_model=DimCustomerDTO,
    summary="Get one customer",
    description="Fetch a single customer by primary key.",
    response_description="The requested customer.",
    responses={404: {"description": "Customer not found."}},
)
def get_customer(
    customer_id: int,
    session: Session = Depends(get_session),
) -> DimCustomer:
    customer = service.get(session, customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found.")
    return customer
