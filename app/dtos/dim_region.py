from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class DimRegionDTO(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"example": {"id": 1, "region": "southeast"}},
    )

    id: int = Field(description="Primary key in `public.dim_regions`.")
    region: str | None = Field(default=None, description="Region name.")
