# Salary Management Tool

Web app for an HR Manager to manage salaries for 10,000 employees across countries and answer "how do we pay people?".

- **Employees:** search, filter, sort and page through every employee; add, edit and delete; export the filtered view to CSV.
- **Insights:** min, 25th percentile, median, 75th percentile, max and average pay by country, job title or department, plus a salary distribution. Everything is compared in USD at fixed demo rates.

Scope: [docs/requirements.md](docs/requirements.md). Decisions and tradeoffs: [docs/architecture.md](docs/architecture.md). How AI was used: [docs/ai/prompt-log.md](docs/ai/prompt-log.md).

## Live

- App: https://salary-management-assessment-6256.vercel.app
- Backend API: https://salary-management-assessment-omega.vercel.app ([API docs](https://salary-management-assessment-omega.vercel.app/docs))

The API runs as a serverless function. The first request after a quiet period takes about a second while it starts; the app shows a "waking up the server" message if a request takes longer than 3 seconds.

## Run locally

Requirements: Python 3.14, Node.js 20 or newer, Docker.

### Backend

```bash
cd backend
python3.14 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
docker compose up -d db
alembic upgrade head
python -m app.scripts.seed --reset
uvicorn app.main:app --reload
```

The API is at http://localhost:8000 and its docs at http://localhost:8000/docs.

### Frontend

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

The app is at http://localhost:3000. `NEXT_PUBLIC_API_URL` in `.env.local` points at the API; use the live URL above to work against the deployed backend.

## Seed data

`python -m app.scripts.seed --reset` loads 10,000 demo employees across 10 countries. The same `--seed` (default 42) always gives the same data. Without `--reset` the script refuses to run when employees already exist. Use `--count` for a smaller set.

## Tests and checks

```bash
cd backend
pytest                    # unit tests, no database
pytest -m integration     # SQL tests against the Docker database
ruff check . && ruff format --check .

cd frontend
npm run lint && npm run typecheck
```

CI runs the backend lint and unit tests on every push that changes `backend/`.

## Deploy

The backend and frontend are two Vercel projects from this repository.

- **Backend:** root directory `backend`. Vercel detects FastAPI from `app/main.py` and uses Python 3.14 from `.python-version`. Set `DATABASE_URL` to the Supabase transaction pooler URL (port 6543, scheme `postgresql+psycopg://`) and the function region to the database's region.
- **Frontend:** root directory `frontend`. Set `NEXT_PUBLIC_API_URL` to the backend URL.
- **Database:** run `alembic upgrade head` and the seed from your machine with `DATABASE_URL` set to the Supabase session pooler URL (port 5432).
