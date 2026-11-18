-- database/schema/02_dim_product_categories.sql
-- Run order: 2 of 6. No dependencies.

BEGIN;

CREATE TABLE IF NOT EXISTS dim_product_categories (
    id               BIGINT PRIMARY KEY,
    product_category VARCHAR(255)
);

COMMIT;
