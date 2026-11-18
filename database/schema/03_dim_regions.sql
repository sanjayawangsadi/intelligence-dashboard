-- database/schema/03_dim_regions.sql
-- Run order: 3 of 6. No dependencies.

BEGIN;

CREATE TABLE IF NOT EXISTS dim_regions (
    id     BIGINT PRIMARY KEY,
    region VARCHAR(255)
);

COMMIT;
