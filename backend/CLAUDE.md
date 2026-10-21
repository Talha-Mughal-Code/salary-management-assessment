# Salary Management backend — house rules

Applies to all work in `backend/`. The frontend counterpart is `../frontend/CLAUDE.md`, which does not apply here.

## Context — read this before auditing the codebase

- `../docs/requirements.md` is the scope. `../docs/architecture.md` holds decisions and tradeoffs.
- Read only the files your task touches. Do not read the whole codebase to start.
- Durable facts (invariants, gotchas, decisions) go in `../docs/architecture.md`. The debugging story goes in the commit body. `../docs/ai/prompt-log.md` is history, never a source for how the system works.

## Architecture

`router -> service -> repository -> database`
- `app/api/`: routers. HTTP only.
- `app/services/`: business rules and calculations.
- `app/repositories/`: all SQL.
- `app/schemas/`: Pydantic request and response models. `app/models/`: SQLAlchemy tables.
- The repository interface is the one deliberate abstraction, because it lets unit tests use a fake. Add no others without a stated reason.

## Domain rules

- Employee fields: id, full_name, email (unique), job_title, department, country (ISO 3166 alpha-2), currency (ISO 4217), salary, salary_usd, hire_date, created_at, updated_at.
- Money is `Decimal` / `Numeric(12, 2)`. Never float.
- `salary` is local currency. `salary_usd` is computed on write from fixed demo rates in `app/core/fx.py`.
- Insights use `percentile_cont` over `salary_usd`. Never compute medians in Python.
- Lists are always paginated server-side: `page`, `page_size` (default 25, max 100), `q`, `country`, `job_title`, `department`, `sort`, `order`.

## Code rules

1. **No file over 250 lines.** One responsibility per file.
2. **No comments.** Short docstrings only where the *why* is non-obvious. Never a comment explaining what a line does.
3. **Logic lives in `services/`.** No logic in routers, no logic in schemas, no SQL outside repositories.
4. **Imports at the top of the file**, never inside functions, classes or conditionals. Ruff sorts them.
5. **Check the established practice before designing insights logic** (median and percentiles for pay distribution, ISO country and currency codes).
6. **Never hand-write a migration.** Generate it with `alembic revision --autogenerate`, review it, and confirm there is a single Alembic head before committing.
7. **Meaningful names** for every new file, model, schema, service and directory.
8. **Tests are required for every feature and fix.** A fix or behavior change must include a test that fails against the pre-fix code. Do not skip them.
9. **Endpoints are documented in the schema, never in a separate doc file.** Set `summary`, `description`, `response_model` and `tags` on every route. Describe each tag once in `app/api/tags.py`. A test fails if a route has no tag or a tag has no description.
10. **Leave no dead code.** Delete what your change leaves unused: imports, helpers, constants, schemas, tests of removed code. `ruff` unused-import and unused-variable rules must be clean.

## Commits

Conventional Commits (`type(scope): summary`). Never commit `.env`.

## Running things

Activate the venv from `backend/` before running anything: `source .venv/bin/activate`. Settings live in `app/core/config.py`.

- Run API: `uvicorn app.main:app --reload`
- Unit tests: `pytest` (no network, no database)
- Integration tests: `pytest -m integration` (needs local Postgres via `docker compose up -d db`)
- Lint and format: `ruff check . && ruff format --check .`
- Migrations: `alembic upgrade head`
- Seed: `python -m app.scripts.seed --reset`
