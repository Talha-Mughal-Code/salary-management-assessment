# AI prompt log

Record how AI was used and how its output was checked. Add an entry for each notable prompt: planning, design decisions, tricky code, and every time the AI was wrong.

## Template

### Short title
- **Goal:** what I was trying to do
- **Prompt (or summary):** what I asked, including the file used
- **Result:** what the AI produced
- **My review:** what I checked (tests, reading the diff, running it)
- **Correction:** what was wrong or changed, and why (write "none" if none)
- **Commit:** short hash or message

## Entries

### FastAPI skeleton with health endpoint
- **Goal:** start the backend with a runnable app, lint and test config, and one passing test.
- **Prompt (or summary):** asked Claude Code to add a FastAPI app with a `GET /health` endpoint, following `backend/CLAUDE.md`.
- **Result:** `pyproject.toml` (ruff, pytest with integration tests skipped by default), `app/main.py`, `app/api/health.py`, `app/api/tags.py`, `app/schemas/health.py`, `tests/test_health.py`.
- **My review:** `pytest` and `ruff` clean; ran uvicorn and checked `/health` and the tag in `/openapi.json`.
- **Correction:** `app/main.py` went over ruff's line length, so it was fixed with `ruff format`. `tags.py` was added early because rule 9 needs a tag on every route.
- **Commit:** `chore(backend): initialize FastAPI app with health endpoint`

### Backend deployment on Vercel
- **Goal:** deploy the backend skeleton early so hosting problems show up before features exist.
- **Prompt (or summary):** asked Claude Code for a Render Blueprint for the FastAPI backend, then to move the backend to Vercel when Render asked for a card.
- **Result:** `backend/.python-version` (3.14), README deploy notes, and updated hosting decisions in `docs/architecture.md` and `docs/requirements.md`. Vercel detects FastAPI from `app/main.py`, so no `vercel.json` is needed.
- **My review:** checked the entrypoint and Python version rules in Vercel's FastAPI and Python runtime docs; `pytest` and `ruff` clean.
- **Correction:** the first version used Render, but its free plan (Blueprint and manual web service) asked for a card. Switched to Vercel Hobby, which does not. Serverless means each instance opens its own connections, so the database will go through Supabase's pooler with `NullPool`.
- **Commit:** `chore(deploy): set up backend deployment on Vercel`

### Vercel build failed on pyproject.toml
- **Goal:** fix the first Vercel build.
- **Prompt (or summary):** pasted the build log: `uv lock` failed with "No `project` table found in pyproject.toml".
- **Result:** moved the ruff settings to `ruff.toml` and the pytest settings to `pytest.ini`, and deleted `pyproject.toml`, so Vercel installs from `requirements.txt`.
- **My review:** `pytest` and `ruff` still pick up their settings; redeployed, and `/health` on the live URL returns ok.
- **Correction:** the earlier Vercel setup missed that Vercel prefers `pyproject.toml` over `requirements.txt` when both exist.
- **Commit:** `fix(deploy): move tool config out of pyproject.toml for Vercel`

### Settings and database session
- **Goal:** read the database URL from settings and give the app a session that works on Vercel with Supabase.
- **Prompt (or summary):** asked Claude Code for `pydantic-settings` config, a SQLAlchemy engine and session, `.env.example`, and a local Postgres in Docker.
- **Result:** `app/core/config.py`, `app/core/database.py` (`NullPool`, prepared statements off for Supabase's transaction pooler), `docker-compose.yml` with Postgres 17, `.env.example`, unit tests for settings and pooling, and an integration test that runs `SELECT 1`.
- **My review:** `pytest`, `pytest -m integration` against the Docker database, and `ruff` all clean. Settings and engine are created on first use, so importing the app without `DATABASE_URL` does not fail.
- **Correction:** none
- **Commit:** `feat(backend): add settings and database session setup`

### Employee model and first migration
- **Goal:** create the `employees` table with the indexes the list filters need.
- **Prompt (or summary):** agreed the columns, types and indexes with Claude Code first (integer identity id, unique lowercase email, `numeric(12,2)` money, `salary > 0` check), then asked it to add the model and Alembic setup and autogenerate the migration.
- **Result:** `app/models/base.py` (constraint naming convention), `app/models/employee.py`, `alembic.ini` with ruff hooks for new migrations, `alembic/env.py` reading the URL from settings, the migration, and unit tests on the table definition.
- **My review:** read the generated migration; ran upgrade, `\d employees`, downgrade and upgrade again against Docker Postgres; one head; `alembic check` reports no drift; `pytest` and `ruff` clean.
- **Correction:** ruff sorted `from alembic import ...` as first-party because of the local `alembic/` folder, so `alembic` is marked third-party in `ruff.toml`. Indexes for name search and salary sorting are left for the performance pass.
- **Commit:** `feat(backend): add Employee model and initial migration`

### Fixed exchange rates
- **Goal:** convert local salaries to USD so insights compare one currency.
- **Prompt (or summary):** agreed 8 currencies (USD, EUR, GBP, CAD, AUD, JPY, INR, BRL) for 10 countries with Claude Code, then asked for `app/core/fx.py` with `Decimal` maths and tests.
- **Result:** `USD_PER_UNIT` rate table, `to_usd()` rounding half-up to cents, `UnknownCurrencyError`, and unit tests.
- **My review:** tests cover pass-through, a normal conversion, JPY, a half-cent case (`1000.25 AUD → 660.165`) where half-up and banker's rounding differ, two decimal places, and an unknown currency. `pytest` and `ruff` clean.
- **Correction:** none
- **Commit:** `feat(backend): add fixed FX rates and salary normalization`

