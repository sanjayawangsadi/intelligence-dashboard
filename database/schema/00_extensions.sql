-- database/schema/00_extensions.sql
-- Run first, before 1 of 6.
-- Requires a PostgreSQL build with pgvector available
-- (docker compose uses pgvector/pgvector:pg17).

BEGIN;

CREATE EXTENSION IF NOT EXISTS vector;

COMMIT;
