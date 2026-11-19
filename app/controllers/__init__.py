from app.controllers.dim_customer_controller import router as dim_customer_router
from app.controllers.dim_payment_controller import router as dim_payment_router
from app.controllers.dim_product_category_controller import (
    router as dim_product_category_router,
)
from app.controllers.dim_region_controller import router as dim_region_router
from app.controllers.fact_order_controller import router as fact_order_router

routers = (
    dim_customer_router,
    dim_product_category_router,
    dim_region_router,
    dim_payment_router,
    fact_order_router,
)

__all__ = ["routers"]
