# Architecture and tradeoffs

Status: draft. Finalized once the build is complete.

Scope lives in [requirements.md](requirements.md). This note records how the system is built and why.

## Shape

```
Browser -> Next.js (Vercel) -> FastAPI (Render) -> Postgres (Supabase)
```

A modular monolith: one backend, one database, clear internal layers. 10,000 rows, one user and a small team do not justify services that deploy separately.

Backend layers: `router -> service -> repository -> database`.

- Routers handle HTTP only.
- Services hold business rules and calculations.
- Repositories hold all SQL.
- The repository interface is the one deliberate abstraction. It lets service tests run against an in-memory fake, with no database.

## Decisions

| Decision | Choice | Alternative considered | Why |
| --- | --- | --- | --- |
| Backend | FastAPI, SQLAlchemy, Alembic | Next.js full-stack (API routes and an ORM) | Typed request models, OpenAPI docs for free, and a clean layer for unit tests. Cost: two deploys and CORS. |
| Database | Postgres on Supabase | SQLite | Free hosts have ephemeral filesystems. Postgres has `percentile_cont` built in. |
| Hosting | Render (backend), Vercel (frontend) | One platform for both | Free tier for each part. Render sleeps after idle, so the UI shows a "waking up the server" message. |
| Money | `Decimal` and `Numeric(12, 2)` | Float | Floats cannot represent cents exactly. |
| Currency | Local `salary` plus ISO 4217 `currency`, and `salary_usd` computed on write | Convert at query time, or live rates | Insights compare in one currency and stay indexable. Fixed demo rates in `app/core/fx.py` keep tests deterministic. Changing a rate means recomputing `salary_usd`. |
| Pay insights | Median and percentiles with `percentile_cont` in SQL | Averages only, or computing in Python | Pay is skewed, so medians describe it better than averages. Computing in SQL avoids loading 10,000 rows into the app. |
| Lists | Server-side pagination, search, filters and sort | Load everything into the browser | Keeps the page fast at 10,000 rows. Indexes on `country`, `job_title` and `department`, and a unique index on `email`. |
| Frontend API types | Written by hand in `src/types/`, matching the backend schemas | Generated from OpenAPI | A handful of endpoints does not justify a codegen step. Types are updated in the same change as the endpoint. |
| Testing | Unit tests on services with a fake repository, plus integration tests against local Postgres | Mostly end-to-end tests | Unit tests run in seconds with no network. Integration tests cover the SQL. |

## Left out

See "Deliberately left out" in [requirements.md](requirements.md).
