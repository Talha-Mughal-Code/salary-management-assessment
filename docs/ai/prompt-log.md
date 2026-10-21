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

