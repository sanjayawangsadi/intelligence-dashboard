-- database/schema/01_dim_customers.sql
-- Run order: 1 of 6. No dependencies.

BEGIN;

CREATE TABLE IF NOT EXISTS dim_customers (
    id                 BIGINT PRIMARY KEY,
    customer_unique_id BIGINT
);

COMMIT;
