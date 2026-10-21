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

### Seed script for 10,000 employees
- **Goal:** load realistic, reproducible demo data in one command.
- **Prompt (or summary):** asked Claude Code for a deterministic seed script: weighted countries and departments, title-based salaries scaled per country, unique emails, chunked bulk insert and a `--reset` guard.
- **Result:** `app/scripts/seed_data.py` (countries, departments, US base salary per title), `app/scripts/seed.py` (`generate_employees`, `seed_employees`, CLI), unit tests on the generated data and integration tests that roll back.
- **My review:** unit tests check determinism, count, unique well-formed emails, currency per country, titles per department, `salary_usd`, and hire dates. Ran the real seed locally: 10,000 rows in about 2 seconds, a second run without `--reset` exits 1, and medians by country look sensible (US highest, India and Brazil lowest).
- **Correction:** seeding Faker once gave the English locales identical name sequences, so each locale gets its own seed. Japanese names are romanized so emails stay ASCII.
- **Commit:** `feat(backend): add deterministic seed script for 10,000 employees`

### CI for the backend
- **Goal:** run lint and unit tests on every backend change.
- **Prompt (or summary):** asked Claude Code for a GitHub Actions workflow running `ruff` and `pytest` for `backend/`.
- **Result:** `.github/workflows/backend.yml`: runs on pushes to `main` and pull requests that touch `backend/`, uses Python from `backend/.python-version`, caches pip, then `ruff check`, `ruff format --check` and `pytest`. Integration tests stay local, since plain `pytest` skips them.
- **My review:** checked the `setup-python@v7` inputs and that both `v7` tags exist; ran the same steps on a clean copy of the committed backend with no `.env` or `DATABASE_URL`: all passed.
- **Correction:** none
- **Commit:** `ci: add GitHub Actions for lint and unit tests`

### Employee request and response schemas
- **Goal:** define the API contract for employees and reject bad input before it reaches the service.
- **Prompt (or summary):** agreed the fields and rules with Claude Code first (supported currencies only, two-letter country, positive salary with 2 decimals, partial updates, money as strings), then asked for the Pydantic models and tests.
- **Result:** `app/schemas/employee.py` with `EmployeeCreate`, `EmployeeUpdate` (every field optional, but not null) and `EmployeeResponse`; tests for each rule.
- **My review:** 15 schema tests cover valid input, a missing field, bad salary, currency, country, email and name values, unknown fields, empty and null updates, and money serialized as strings. `pytest` and `ruff` clean.
- **Correction:** Pydantic checks `pattern` before `to_upper`, so lowercase `de` was rejected. The country pattern now accepts either case and the value is still stored uppercase. Email uses a simple pattern instead of `EmailStr` to avoid adding `email-validator`.
- **Commit:** `feat(backend): add employee schemas with validation`

### Employee repository and service
- **Goal:** create, read, update and delete employees, with business rules in the service and SQL in the repository.
- **Prompt (or summary):** asked Claude Code for a repository interface, a SQLAlchemy implementation, an `EmployeeService` with domain errors, and a fake repository for unit tests.
- **Result:** `EmployeeRepository` protocol, `SqlAlchemyEmployeeRepository` (commits each write), `EmployeeService` (lowercases email, rejects duplicates, recomputes `salary_usd` on every update), `EmployeeNotFoundError` and `DuplicateEmailError`, `tests/fakes.py`, 11 service unit tests, 4 repository integration tests, and a shared savepoint fixture so integration tests never change local data.
- **My review:** `pytest`, `pytest -m integration` and `ruff` clean; the 10,000 seeded rows were still there after the integration run.
- **Correction:** a repository test asserted that `updated_at` increases, but `now()` is fixed inside one transaction, so it could never fail. Removed that assertion. The duplicate-email check runs before the insert; the unique index still protects against a race.
- **Commit:** `feat(backend): add employee repository and service for CRUD`

