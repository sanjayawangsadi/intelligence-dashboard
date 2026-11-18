-- database/schema/04_dim_payments.sql
-- Run order: 4 of 6. No dependencies.

BEGIN;

CREATE TABLE IF NOT EXISTS dim_payments (
    id      BIGINT PRIMARY KEY,
    payment VARCHAR(255)
);

COMMIT;
