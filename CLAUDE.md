# CLAUDE.md

Behavioral guidelines to reduce common LLM coding mistakes, followed by project-wide instructions. Area rules live in `backend/CLAUDE.md` and `frontend/CLAUDE.md`.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.

---

# Project: Salary Management Tool

Web app for an HR Manager at ACME to manage salaries for 10,000 employees across countries and to answer "how do we pay people?". Monorepo: `backend/` (FastAPI), `frontend/` (Next.js), `docs/`.

## Context

- `docs/requirements.md`: scope. If a request is not in it, ask first.
- `docs/architecture.md`: decisions and tradeoffs. Add a line there for any non-obvious decision.
- `docs/ai/prompt-log.md`: history of AI use. Not a source for how the system works.
- Read only the files your task touches. Do not audit the whole repo.

## Response Rules

- Prefer the smallest possible response.
- Show changed snippets or diffs, not whole files.
- Do not repeat the user's prompt or existing code.
- Do not add filler or summaries of what was just done.
- Assumptions, ambiguity and tradeoffs are the exception: state them briefly (see rule 1).

## Ask First

- Adding new dependencies (npm or Python).
- Changing the database schema or the API contract.
- Changing deployment configuration (Vercel settings).
- Anything not covered by `docs/requirements.md`.

## Never

- Never commit secrets, credentials, or `.env` files. Commit `.env.example` only.
- Never run commands against a production database. Local and dev databases only.
- Never edit generated output or dependency folders.
- Never skip tests to make a change pass.

## Definition of done

1. Success criteria were stated up front (rule 4) and are verified by tests.
2. Backend: `pytest` passes and `ruff` is clean. Frontend: `npm run lint` and `npm run typecheck` are clean.
3. Behavior matches `docs/requirements.md`.
4. One small commit, Conventional Commits style.
5. Notable AI prompts and any corrections are noted in `docs/ai/prompt-log.md`.
