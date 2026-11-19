from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class DimPaymentDTO(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"example": {"id": 1, "payment": "credit_card"}},
    )

    id: int = Field(description="Primary key in `public.dim_payments`.")
    payment: str | None = Field(default=None, description="Payment method name.")
