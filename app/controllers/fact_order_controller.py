from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from config.database import get_session
from app.models import FactOrder
from app.dtos.fact_order import FactOrderDTO
from app.dtos.pagination import PageDTO
from app.services.fact_order_service import FactOrderService

router = APIRouter(prefix="/orders", tags=["orders"])
service = FactOrderService()


@router.get(
    "",
    response_model=PageDTO[FactOrderDTO],
    summary="List orders",
    description="Return orders ordered by primary key.",
    response_description="A page of orders.",
)
def list_orders(
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
    "/{order_id}",
    response_model=FactOrderDTO,
    summary="Get one order by order id",
    description="Fetch a single order by its business order id, not the surrogate id.",
    response_description="The requested order.",
    responses={404: {"description": "Order not found."}},
)
def get_order(
    order_id: int,
    session: Session = Depends(get_session),
) -> FactOrder:
    order = service.get_by_order_id(session, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found.")
    return order
