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

### Employee CRUD endpoints
- **Goal:** expose create, get, update and delete over HTTP with clear errors and documented routes.
- **Prompt (or summary):** asked Claude Code for routers under `/api/v1/employees`, error handlers for 404 and 409, an `employees` tag, and a test that every route has a described tag.
- **Result:** `app/api/employees.py`, `app/api/dependencies.py` (service built from the request session), `app/api/errors.py` (404 and 409 handlers and documented error responses), `app/schemas/error.py`, the `employees` tag, router tests using the fake repository, and route documentation tests (tag, summary, description).
- **My review:** `pytest` and `ruff` clean. Ran uvicorn against the seeded Docker database and called each route with curl: 201, 409 on a duplicate email in another case, 200, `salary_usd` and `updated_at` change on PATCH, 204, then 404, and 422 for a non-numeric id. Checked `/openapi.json` lists the tag and error codes for each route.
- **Correction:** the fake repository needed `created_at` and `updated_at`, since the response model requires them.
- **Commit:** `feat(backend): add employee CRUD endpoints`

### Paginated employee list
- **Goal:** list 10,000 employees one page at a time, with search, filters and sorting on the server.
- **Prompt (or summary):** asked Claude Code for `GET /api/v1/employees` with `page`, `page_size`, `q`, country, job title and department filters, `sort` and `order`.
- **Result:** `EmployeeListParams` and `EmployeePage` schemas, `search` in the repository (one count query plus one page query, ties ordered by id, `q` escaped), a pass-through in the service, the route, router and service tests, and integration tests on a known set of rows.
- **My review:** `pytest`, `pytest -m integration` and `ruff` clean. Checked that the `%` search test fails when escaping is removed. Against 10,000 seeded rows, warm requests took 16 to 31 ms.
- **Correction:** the first escape test searched for `100%`, which passes even without escaping, so it now searches for `%`. While checking that, a `git checkout` reverted the repository file and it had to be rewritten. Accented names sort after Z locally because the Alpine Postgres image compares bytes; noted for the performance pass.
- **Commit:** `feat(backend): add paginated employee list with search and filters`

### Pay insights summary
- **Goal:** answer "how do we pay people?": pay statistics by country, job title or department, in USD.
- **Prompt (or summary):** agreed the endpoint shape with Claude Code first (`group_by` plus the list filters; overall and per-group headcount, min, p25, median, p75, max and average), then asked for the schema, repository, service, route and tests.
- **Result:** `GET /api/v1/insights/summary`, `app/schemas/insights.py`, `SqlAlchemyInsightsRepository` using `percentile_cont` cast back to `numeric(12,2)`, `InsightsService` ordering groups by median, an `insights` tag, and a shared `apply_employee_filters` helper now used by the list too.
- **My review:** integration tests compare SQL results with values worked out by hand, including interpolated percentiles (17,500 between 10,000 and 20,000), filters applied before grouping, and an empty result. On the seeded data, the German Staff Engineer median from the API matched a direct `percentile_cont` query in psql. `pytest` and `ruff` clean.
- **Correction:** none. Kept p25 and p75 only; p10 and p90 can be added later.
- **Commit:** `feat(backend): add pay insights by country, job title and department`

### Salary distribution
- **Goal:** give the dashboard a histogram of salaries in USD.
- **Prompt (or summary):** asked Claude Code for `GET /api/v1/insights/distribution` with the same filters as the summary, about 20 buckets with round edges, counted in SQL.
- **Result:** `SalaryDistribution` and `SalaryBucket` schemas, `salary_range` and `bucket_counts` in the insights repository, bucket sizing in `InsightsService` (`nice_width` picks 1, 2, 2.5 or 5 times a power of ten), and the route.
- **My review:** unit tests cover `nice_width`, bucket edges, the bucket holding the maximum, empty buckets, a single salary, no employees, and money serialized as plain strings. Integration tests check the SQL range and counts. On the seeded data, bucket totals match headcounts (10,000 overall, 1,149 for Germany). `pytest` and `ruff` clean.
- **Correction:** counts use `floor((salary - start) / width)` instead of `width_bucket`, which needs special handling for a value equal to the upper bound. Rounding the width up gives 13 to 19 buckets on real data, so the description now says "up to about 20".
- **Commit:** `feat(backend): add salary distribution insight`

### CSV export
- **Goal:** let the HR Manager download the filtered employee view.
- **Prompt (or summary):** asked Claude Code for `GET /api/v1/employees/export` reusing the list's search, filters and sort, without paging.
- **Result:** `EmployeeQuery` (list parameters without paging, now the base of `EmployeeListParams`), `all_matching` in the repository, `employees_to_csv` with formula-injection protection, `export_csv` in the service, and the route, declared before `/{employee_id}` so `export` is not read as an id.
- **My review:** unit tests cover the header, plain values, commas and quotes, formula-like text, the download headers, filtering and the route order; an integration test covers the SQL. Exported all 10,000 seeded rows: 1.8 MB in 0.39 s. `pytest` and `ruff` clean.
- **Correction:** the plan said streaming; rows are loaded in one query instead, because a streamed response would need the database session to outlive the request. The file stays under Vercel's 4.5 MB response limit.
- **Commit:** `feat(backend): add CSV export for the filtered employee view`


### CORS for the frontend
- **Goal:** let the browser app call the API from another origin.
- **Prompt (or summary):** asked Claude Code to enable CORS for the frontend.
- **Result:** `CORSMiddleware` allowing any origin without credentials, for `GET`, `POST`, `PATCH` and `DELETE` with JSON bodies, and two tests (a `PATCH` preflight and a simple `GET`).
- **My review:** `pytest` and `ruff` clean; checked the headers with curl against a local server.
- **Correction:** none. Any origin is acceptable only because there is no login or cookies; this is recorded in `docs/architecture.md` together with what changes when login is added.
- **Commit:** `feat(backend): allow cross-origin requests from the frontend`

### Frontend
- **Goal:** the HR Manager's UI: employee directory with search, filters, sorting, paging, create, edit, delete and CSV export, plus the insights dashboard.
- **Prompt (or summary):** asked Claude Code to build the rest of the frontend following `frontend/CLAUDE.md`, after reading the bundled Next.js 16 docs on Cache Components and `useSearchParams`.
- **Result:** typed API client (`src/lib/api.ts`), formatters, `useApiData` (loading, errors, and a "waking up the server" flag after 3 seconds), `useEmployeeQuery` (list state in the URL), `useFilterOptions`, the directory components, form and delete dialogs, and the insights dashboard with a CSS histogram. shadcn components added with the CLI. No new npm dependencies.
- **My review:** `npm run lint`, `npm run typecheck` and `npm run build` pass; ran the app locally against the local API and checked each request the UI makes with curl (list, filters, preflight, 422 shape).
- **Correction:** a sort header component was first defined inside the table component, which React recreates on every render; moved it out. `npm run format` also reformatted three files that were already in the repo, so those changes were reverted. Pydantic's pattern errors were unreadable, so the client shows "Has an invalid format." instead. The UI was not checked in a browser.
- **Commit:** see the frontend commits in the commit list.
