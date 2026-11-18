-- database/schema/run_all.sql
-- Runs every DDL file in dependency order, stopping at the first error.
-- Usage: psql -d <database> -f database/schema/run_all.sql

\set ON_ERROR_STOP on

\ir 00_extensions.sql
\ir 01_dim_customers.sql
\ir 02_dim_product_categories.sql
\ir 03_dim_regions.sql
\ir 04_dim_payments.sql
\ir 05_fact_orders.sql
\ir 06_indexes.sql
