from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class DimCustomerDTO(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"example": {"id": 1, "customer_unique_id": 10001}},
    )

    id: int = Field(description="Primary key in `public.dim_customers`.")
    customer_unique_id: int | None = Field(
        default=None,
        description="Stable customer identifier from the source dataset.",
    )
