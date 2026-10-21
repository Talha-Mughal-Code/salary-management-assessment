# Salary Management Tool — Requirements

## Goal and user

Give ACME's HR Manager one web app to manage salaries for 10,000 employees across several countries, replacing today's Excel files, and to answer "how do we pay people?" in seconds. The single user is the HR Manager, who needs to find, edit and compare pay data and spot gaps or outliers without building spreadsheets.

## Scope and features

Six features, each tied to something the HR Manager does today in Excel.

| Feature | What it does | Why it is in |
| --- | --- | --- |
| Employee directory | Paginated list with search, filters (country, job title, department) and sorting, all server-side | 10,000 rows must stay fast and usable |
| Employee create, edit, delete | Form with validation (required fields, positive salary, valid currency) | Replaces editing cells in a spreadsheet |
| Pay insights | Min, median, average, max and percentiles by country, job title and department, plus a salary distribution | Directly answers "how do we pay people?" |
| Multi-currency | Each salary stored in local currency; insights compare in USD using fixed demo rates | Employees are in several countries |
| CSV export | Download the current filtered view | Lets HR take data back to Excel when needed |
| Seed script | Generates 10,000 realistic, reproducible employees | Required for the assessment and for demos |

## Deliberately left out

These are real needs in production, but each adds scope without proving the core value, which is managing and understanding pay.

| Left out | Reason |
| --- | --- |
| Login and roles | One persona, so access control adds work without testing the core idea. The demo uses fake data only. |
| Salary history and audit trail | Valuable, but it roughly doubles the data model. First candidate for a next version. |
| CSV import | The seed script loads the data, and import needs a full validation and error-reporting experience. |
| Bonuses, equity, benefits, payroll, tax | The question is about base salary. |
| Live exchange rates | Fixed demo rates keep insights and tests deterministic. |
| Approvals, notifications, org hierarchy | They need multiple users and workflows that this persona does not have. |

## Key decisions and constraints

The design is deliberately simple: one backend, one database, clear internal layers.

| Decision | Choice | Why |
| --- | --- | --- |
| Architecture | Modular monolith: router, service, repository layers | 10,000 rows, one user and a small team do not justify microservices |
| Backend | FastAPI, SQLAlchemy, Alembic migrations (Python) | Typed, testable, auto-generated API docs |
| Database | Supabase Postgres | Free hosting filesystems are ephemeral, and Postgres has built-in percentile functions for insights |
| Frontend | Next.js, TypeScript, shadcn/ui, server-side pagination | Never load all 10,000 rows into the browser |
| Deployment | Monorepo: backend and frontend as two Vercel projects, database on Supabase | Free tier with no card; a cold start after idle time is documented in the README |
| Currency | Local amount plus ISO currency code per employee; insights in USD | Fair comparison across countries |
| Performance targets | List and search under 300 ms, insights under 1 s, at 10,000 rows | Indexed queries; measured and noted in the performance notes |
| Testing | pytest on the service layer with fakes, no network, fixed random seed | Fast, deterministic, easy to read |
| AI use | CLAUDE.md and a prompt log in docs/ai/ | Shows intentional AI use and how its output was checked |

## Success criteria

The product works if the HR Manager can do the following without leaving the app.

- Answer "what is the median salary for each job title in Germany?" in under a minute
- Find any employee by name or country and update their salary in a few clicks
- Spot the highest and lowest paid groups by country and department
- Export a filtered view to CSV

The delivery works if the seed script loads 10,000 employees in one command, the unit tests run in seconds, the app is live at a public URL, and the commit history, design notes and prompt log show how it was built.
