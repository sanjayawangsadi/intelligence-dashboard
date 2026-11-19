from fastapi import FastAPI

from app.controllers import routers
from app.core import register_error_logger, setup_logging

setup_logging()

TAGS_METADATA = [
    {
        "name": "customers",
        "description": "Customer dimension: `public.dim_customers`.",
    },
    {
        "name": "product-categories",
        "description": "Product category dimension: `public.dim_product_categories`.",
    },
    {
        "name": "regions",
        "description": "Region dimension: `public.dim_regions`.",
    },
    {
        "name": "payments",
        "description": "Payment method dimension: `public.dim_payments`.",
    },
    {
        "name": "orders",
        "description": "Order facts: `public.fact_orders`.",
    },
]

app = FastAPI(
    title="Intelligence Dashboard",
    description=(
        "Read-only analytics API over the DWH tables in the `public` schema.\n\n"
        "Collection endpoints accept `limit` and `offset` query parameters. "
        "Orders are addressed by their business `order_id`."
    ),
    version="1.0.0",
    openapi_tags=TAGS_METADATA,
    swagger_ui_parameters={
        "displayRequestDuration": True,
        "filter": True,
        "persistAuthorization": True,
        "defaultModelsExpandDepth": 1,
    },
)

register_error_logger(app)

for router in routers:
    app.include_router(router)
