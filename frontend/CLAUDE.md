# Salary Management Frontend Agent Rules

Applies when working in `frontend/`. The backend counterpart is `../backend/CLAUDE.md`, which does not apply here.

# Refactoring Rules

- Prefer reducing lines of code.
- Prefer removing code over adding abstractions.
- Prefer extracting shared logic only when reused 3+ times.
- Avoid creating new files unless necessary.
- Avoid creating new hooks for simple logic.
- Avoid creating new components for simple JSX.
- Prefer early returns.
- Prefer direct expressions over temporary variables.
- Prefer existing utilities over new helpers.

# Token Optimization

- Never explain generated code.
- Never repeat existing code when only a small part changes.
- Show diffs or changed snippets instead of full files whenever possible.
- Use bullet points only when necessary.

## Project Context

- Frontend is a Next.js (App Router) app in a monorepo with a FastAPI backend.
- Use `npm` only. Do not use `yarn` or `pnpm`.
- Prefer existing project patterns over introducing new architectural styles.

## Structure (flat, no layers)

- `src/app/`: routes. Keep route files thin.
- `src/components/`: feature components. `src/components/ui/`: shadcn primitives, added with the shadcn CLI.
- `src/lib/`: API client (`api.ts`), formatters (`format.ts`), utilities.
- `src/hooks/`: custom hooks. `src/types/`: API request and response types.
- Import from the owning file with `@/` paths. No barrel files, no `export * from`, no one-file passthroughs.

## Commands

- `npm install`
- `npm run dev`
- `npm run build`
- `npm run lint`
- `npm run typecheck`
- `npm run format`
- `npm run format:check`

## TypeScript

- Strict TypeScript only. Never use `any` or `@ts-ignore`.
- Reuse the API types in `src/types/` before creating new ones.
- Prefer explicit payload and response types end to end.
- Use `unknown` plus narrowing when a value is truly unknown.
- Keep assertions minimal and local.
- Prefer a single typed draft object for forms instead of many parallel state primitives.
- Prefix intentionally unused variables with `_`.

## React

- Use function components and hooks only.
- Keep all hooks at the top of the component body before handlers and branching logic.
- Keep business logic out of JSX. Move computations and transformations into helpers or custom hooks.
- Prefer `useCallback` for handlers passed to children. Avoid inline callbacks in JSX unless trivial.
- Do not use effects to mirror props into state unless synchronization is genuinely required.
- Do not leave `console.log` in components.
- Remove unused state, dead branches and leftover helpers during refactors.
- Split large components early into smaller components or hooks.

## File Conventions

- Reusable UI and logic live outside route files.
- Prefer one component per file.
- PascalCase filenames for components, camelCase for hooks.
- No file over 250 lines.

## Data And State

- Keep source-of-truth state minimal and derive the rest.
- Page, page size, search, filters and sort live in URL search params.
- Never fetch, filter or sort all employees in the browser. The server paginates.
- Keep API interaction in `lib/api.ts` and hooks, not inside JSX-heavy components.
- Handle loading, empty and error states for every async view. Show a "waking up the server" message when a request takes longer than 3 seconds.

## Styling And UI

- Reuse shadcn primitives and existing app patterns before building new abstractions.
- Use Tailwind utility classes.
- Use `lucide-react` for icons.
- Keep product copy concise and consistent.

## API Rules

- Do not hardcode URLs. The base URL comes from `NEXT_PUBLIC_API_URL`.
- One shared API client in `src/lib/api.ts`. No ad hoc `fetch` calls elsewhere.
- Normalize and surface user-facing errors consistently (409 duplicate email, 422 validation).

## Git Workflow

- Use conventional commit style.

## Always

- Prefer existing project conventions over introducing new libraries or patterns.
- Run lint and typecheck after substantive changes and fix newly introduced issues.
- Keep implementations simple, typed and maintainable.

## Ask First

- Adding new npm dependencies.
- Changing the shared API client behavior.
- Changing the API contract the UI depends on.

## Never

- Never use `any`.
- Never use `@ts-ignore`.
- Never hardcode backend URLs.
- Never create ad hoc duplicate API clients.
- Never edit generated output or dependency folders.
- Never hardcode currency symbols or codes in user-facing copy. Use the formatters in `src/lib/format.ts`.
- Never do currency conversion in the frontend. USD values come from the API.
- Never commit secrets, credentials or `.env` files.
