from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class DimProductCategoryDTO(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"example": {"id": 1, "product_category": "electronics"}},
    )

    id: int = Field(description="Primary key in `public.dim_product_categories`.")
    product_category: str | None = Field(
        default=None,
        description="Product category name.",
    )
