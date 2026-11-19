from __future__ import annotations

from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class FactOrderDTO(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "order_id": 1001,
                "order_date": "2024-01-15",
                "customer_id": 1,
                "product_category_id": 2,
                "region_id": 3,
                "quantity": 2,
                "unit_price": "49.90",
                "discount": "0.1000",
                "payment_id": 1,
                "delivery_days": 4,
                "customer_rating": 5,
                "revenue": "89.82",
            }
        },
    )

    id: int = Field(description="Surrogate primary key in `public.fact_orders`.")
    order_id: int | None = Field(
        default=None,
        description="Business order identifier, unique across the table.",
    )
    order_date: date | None = Field(default=None, description="Date the order was placed.")
    customer_id: int = Field(
        description="Foreign key to `public.dim_customers.id`."
    )
    product_category_id: int | None = Field(
        default=None,
        description="Foreign key to `public.dim_product_categories.id`.",
    )
    region_id: int | None = Field(
        default=None,
        description="Foreign key to `public.dim_regions.id`.",
    )
    quantity: int | None = Field(default=None, description="Units ordered.")
    unit_price: Decimal | None = Field(
        default=None,
        description="Price per unit before discount.",
    )
    discount: Decimal | None = Field(
        default=None,
        description="Discount rate applied to the line (0-1).",
    )
    payment_id: int | None = Field(
        default=None,
        description="Foreign key to `public.dim_payments.id`.",
    )
    delivery_days: int | None = Field(
        default=None,
        description="Days between order and delivery.",
    )
    customer_rating: int | None = Field(
        default=None,
        description="Customer rating for the order (1-5).",
    )
    revenue: Decimal | None = Field(
        default=None,
        description="Net revenue after discount.",
    )
