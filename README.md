# Intelligence Dashboard

Read-only analytics API over an e-commerce sales data warehouse running on
PostgreSQL. The ETL pipeline loads a CSV dataset into a star schema, and the
FastAPI service exposes the dimensions and facts as JSON endpoints.

## Stack

- Python 3.12, managed with [uv](https://docs.astral.sh/uv/)
- FastAPI + SQLAlchemy 2.1 (psycopg 3 driver)
- PostgreSQL 17 (`pgvector/pgvector:pg17` image)
- Docker Compose

## Project layout

```text
app/
  core/            logging setup and unhandled-exception logging
  controllers/     FastAPI routers (GET only)
  dtos/            Pydantic response DTOs, including PageDTO
  models/          SQLAlchemy ORM models for the public schema
  repositories/    read queries: list, get, count
  services/        read services and pagination
config/
  settings.py      .env loading and DSN construction
  database.py      SQLAlchemy engine, SessionLocal, get_session
database/
  dataset/         source CSV
  etl/             extract, transform, load pipeline
  schema/          DDL applied in dependency order
scripts/
  run_schema.py    apply database/schema/*.sql
  run_etl.py       load the CSV into PostgreSQL
```

## Data model

Star schema in the PostgreSQL `public` schema:

- `dim_customers`
- `dim_product_categories`
- `dim_regions`
- `dim_payments`
- `fact_orders` — foreign keys to every dimension, unique `order_id`,
  indexes on all foreign keys and `order_date`

`database/schema/00_extensions.sql` enables the `vector` extension. The DWH
tables stay in `public`, leaving other schemas free for future vector/embedding
tables.

## Agentic RAG routing (planned)

A planned query layer will analyze each user question with an agentic RAG
workflow and choose the retrieval path before answering:

- **DWH route** — analytical questions about orders, revenue, customers,
  regions, payments, or trends are translated into SQL against the `public`
  star schema. The agent inspects the schema, runs the query, and validates the
  result.
- **Vector route** — semantic or unstructured questions, such as product
  descriptions, reviews, or policy documents, are answered by similarity search
  over embeddings stored in a separate `vector` schema using pgvector.
- **Combined route** — questions that need structured metrics plus semantic
  context use both retrievals and merge the results into one answer.

The router selects the route from the question's intent, then the agent calls
the matching tool (SQL executor or vector search) and returns the answer with
the evidence used. The `vector` extension is already enabled; the agent,
embedding pipeline, and vector schema are not implemented yet.

## Quick start

### Docker

```bash
cp .env.example .env
docker compose up -d --build
```

The app container applies the schema, runs the ETL (skipping it when
`fact_orders` already contains rows), then starts Uvicorn on port 8000.
Application logs are persisted to `./logs`; PostgreSQL data lives in
`./database/data`.

### Local

```bash
cp .env.example .env
docker compose up -d db
uv sync
uv run python scripts/run_schema.py
uv run python scripts/run_etl.py
uv run uvicorn app.main:app --reload
```

## Configuration

Settings are read from `.env` (without overriding real environment variables)
or from the process environment.

| Variable | Default | Purpose |
| --- | --- | --- |
| `DB_HOST` | `localhost` | PostgreSQL host |
| `DB_PORT` | `5432` | PostgreSQL port |
| `DB_NAME` | `intelligence_dashboard` | Database name |
| `DB_USER` | `postgres` | Database user |
| `DB_PASSWORD` | `postgres` | Database password |
| `DATABASE_URL` | — | Full DSN; overrides the `DB_*` values |
| `LOG_LEVEL` | `INFO` | Root and `app` logger level |
| `LOG_FILE` | `logs/app.log` | Log file path; relative paths resolve from the project root |

## API

Base URL: `http://localhost:8000`

- Swagger UI: `/docs`
- ReDoc: `/redoc`
- OpenAPI spec: `/openapi.json`

All endpoints are `GET`:

| Path | Description |
| --- | --- |
| `/customers` | List customers |
| `/customers/{customer_id}` | Get one customer by primary key |
| `/product-categories` | List product categories |
| `/product-categories/{category_id}` | Get one product category |
| `/regions` | List regions |
| `/regions/{region_id}` | Get one region |
| `/payments` | List payments |
| `/payments/{payment_id}` | Get one payment |
| `/orders` | List orders |
| `/orders/{order_id}` | Get one order by business `order_id` |

### Pagination

List endpoints accept `page` (1-based, default `1`) and `page_size`
(default `100`, maximum `500`). The backend computes the offset, row count,
and page metadata:

```json
{
  "items": [],
  "page": 1,
  "page_size": 100,
  "total": 5000,
  "total_pages": 50,
  "has_next": true,
  "has_previous": false
}
```

Examples:

```bash
curl "http://localhost:8000/customers?page=1&page_size=10"
curl "http://localhost:8000/orders/1"
```

Missing rows return `404` with `{"detail": "..."}`. Validation errors return
`422`. Unhandled errors are logged with a traceback and return
`500 {"detail": "Internal server error."}`.

## ETL

`scripts/run_etl.py` reads `database/dataset/ecommerce_sales_analytics_5000.csv`,
validates and types every row, builds the dimensions (stable IDs assigned from
sorted distinct names), and upserts dimensions then facts in one transaction.
Re-running is safe. By default the script skips the load when `fact_orders`
already has rows.

Options:

```bash
uv run python scripts/run_etl.py --csv path/to/file.csv --dsn postgresql://...
```

## Schema management

`scripts/run_schema.py` applies `database/schema/*.sql` in filename order and
stops at the first failure. Files:

```text
00_extensions.sql
01_dim_customers.sql
02_dim_product_categories.sql
03_dim_regions.sql
04_dim_payments.sql
05_fact_orders.sql
06_indexes.sql
```

To apply the whole set with psql:

```bash
psql -d intelligence_dashboard -f database/schema/run_all.sql
```
