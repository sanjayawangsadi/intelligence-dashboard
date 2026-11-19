from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from config.database import get_session
from app.models import DimPayment
from app.dtos.dim_payment import DimPaymentDTO
from app.dtos.pagination import PageDTO
from app.services.dim_payment_service import DimPaymentService

router = APIRouter(prefix="/payments", tags=["payments"])
service = DimPaymentService()


@router.get(
    "",
    response_model=PageDTO[DimPaymentDTO],
    summary="List payments",
    description="Return payment methods ordered by primary key.",
    response_description="A page of payment methods.",
)
def list_payments(
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
    "/{payment_id}",
    response_model=DimPaymentDTO,
    summary="Get one payment",
    description="Fetch a single payment method by primary key.",
    response_description="The requested payment method.",
    responses={404: {"description": "Payment not found."}},
)
def get_payment(
    payment_id: int,
    session: Session = Depends(get_session),
) -> DimPayment:
    payment = service.get(session, payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found.")
    return payment
