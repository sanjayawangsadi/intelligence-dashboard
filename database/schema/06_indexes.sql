-- database/schema/06_indexes.sql
-- Run order: 6 of 6.
-- REQUIRES database/schema/05_fact_orders.sql.

BEGIN;

CREATE INDEX IF NOT EXISTS idx_fact_orders_customer_id
    ON fact_orders (customer_id);
CREATE INDEX IF NOT EXISTS idx_fact_orders_product_category_id
    ON fact_orders (product_category_id);
CREATE INDEX IF NOT EXISTS idx_fact_orders_region_id
    ON fact_orders (region_id);
CREATE INDEX IF NOT EXISTS idx_fact_orders_payment_id
    ON fact_orders (payment_id);
CREATE INDEX IF NOT EXISTS idx_fact_orders_order_date
    ON fact_orders (order_date);

COMMIT;
