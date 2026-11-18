-- database/schema/05_fact_orders.sql
-- Run order: 5 of 6.
-- REQUIRES database/schema/01_dim_customers.sql through database/schema/04_dim_payments.sql,
-- because its foreign keys reference those tables.

BEGIN;

CREATE TABLE IF NOT EXISTS fact_orders (
    id                  BIGINT PRIMARY KEY,
    order_id            BIGINT,
    order_date          DATE,
    customer_id         BIGINT NOT NULL,
    product_category_id BIGINT,
    region_id           BIGINT,
    quantity            INTEGER,
    unit_price          NUMERIC(12,2),
    discount            NUMERIC(5,4),
    payment_id          BIGINT,
    delivery_days       INTEGER,
    customer_rating     SMALLINT,
    revenue             NUMERIC(12,2),
    CONSTRAINT uq_fact_orders_order_id UNIQUE (order_id),
    CONSTRAINT fk_fact_orders_customer
        FOREIGN KEY (customer_id) REFERENCES dim_customers (id),
    CONSTRAINT fk_fact_orders_product_category
        FOREIGN KEY (product_category_id) REFERENCES dim_product_categories (id),
    CONSTRAINT fk_fact_orders_region
        FOREIGN KEY (region_id) REFERENCES dim_regions (id),
    CONSTRAINT fk_fact_orders_payment
        FOREIGN KEY (payment_id) REFERENCES dim_payments (id)
);

COMMIT;
