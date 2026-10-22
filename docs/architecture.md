# Architecture and tradeoffs

Status: final.

Scope lives in [requirements.md](requirements.md). This note records how the system is built and why.

## Shape

```
Browser --pages--> Next.js (Vercel)
   |
   +--JSON--> FastAPI (Vercel Function, Tokyo) --> Postgres (Supabase, Tokyo)
```

Next.js serves the page shells; the browser calls the API directly for data.

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
| Hosting | Vercel for both, as two projects (`frontend/` and `backend/`) | Render for the backend | Render's free plan asks for a card; Vercel Hobby does not. FastAPI runs as one serverless function, so a cold start takes seconds, not a minute. Each instance opens its own connections, so the backend connects through Supabase's pooler with SQLAlchemy pooling off (`NullPool`). The function region is Tokyo (`hnd1`), next to the database (`ap-northeast-1`), so queries do not cross an ocean. |
| Backend tool config | `ruff.toml` and `pytest.ini` in `backend/` | `pyproject.toml` | Vercel installs dependencies from `pyproject.toml` whenever it exists and fails without a `[project]` table. Dependencies stay in `requirements.txt`. |
| Money | `Decimal` and `Numeric(12, 2)` | Float | Floats cannot represent cents exactly. |
| Currency | Local `salary` plus ISO 4217 `currency`, and `salary_usd` computed on write | Convert at query time, or live rates | Insights compare in one currency and stay indexable. Fixed demo rates in `app/core/fx.py` keep tests deterministic. Changing a rate means recomputing `salary_usd`. Rates are USD per unit (multiply, never divide) and results round half-up to cents. |
| Pay insights | Median and percentiles with `percentile_cont` in SQL | Averages only, or computing in Python | Pay is skewed, so medians describe it better than averages. Computing in SQL avoids loading 10,000 rows into the app. |
| Lists | Server-side pagination, search, filters and sort | Load everything into the browser | Keeps the page fast at 10,000 rows. Indexes on `country`, `job_title` and `department`, and a unique index on `email`. |
| CSV export | Load matching rows in one query, then return the CSV; text cells starting with `=`, `+`, `-` or `@` are prefixed with `'` | Stream rows from the database | A full export of 10,000 rows fits within Vercel's 4.5 MB response limit, and the session does not have to outlive the request. The prefix stops spreadsheets running formulas from employee data. |
| CORS | Any origin, no credentials | A list of allowed frontend origins | There is no login, so the API sends no cookies and CORS is not what protects it; anyone can call it with curl. Allowing any origin avoids per-deployment config for Vercel preview URLs. Adding login would mean restricting origins and allowing credentials. |
| Frontend API types | Written by hand in `src/types/`, matching the backend schemas | Generated from OpenAPI | A handful of endpoints does not justify a codegen step. Types are updated in the same change as the endpoint. |
| Frontend data loading | Client components fetch from the API; list state lives in the URL | Server Components fetching per request | Search, filters and paging respond without a server round trip through Next.js, and the "waking up the server" message can be shown from the browser. Pages are wrapped in `Suspense` because `useSearchParams` needs it with Cache Components. |
| Frontend libraries | No additions beyond the scaffold: forms use one typed draft object, browser validation and the API's 422 errors; the histogram is CSS bars | react-hook-form and zod for forms, a chart library | One form and one chart do not justify three dependencies. The API is the single source of validation rules. |
| Filter options | Countries, departments and job titles come from the insights summary's group names | A dedicated options endpoint | No API change, and the options always match the data. |
| Testing | Unit tests on services with a fake repository, plus integration tests against local Postgres | Mostly end-to-end tests | Unit tests run in seconds with no network. Integration tests cover the SQL. |

## Left out

See "Deliberately left out" in [requirements.md](requirements.md).

## What I would do next

1. Login and roles. Then restrict CORS to the frontend origins and allow credentials.
2. Salary history: an append-only table of salary changes, so insights can show raises over time.
3. Frontend tests for the URL state and the form's error mapping.
4. If the data grew past about 100,000 rows: a `pg_trgm` index for name search and keyset pagination for deep pages.
