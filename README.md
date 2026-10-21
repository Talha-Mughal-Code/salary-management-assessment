# Salary Management Tool

Web app for an HR Manager to manage salaries for 10,000 employees across countries and answer "how do we pay people?".

See [docs/requirements.md](docs/requirements.md) for scope.

## Live

- Backend API: https://salary-management-assessment-mokv.vercel.app ([API docs](https://salary-management-assessment-mokv.vercel.app/docs))

## Deploy

The backend and frontend are two Vercel projects from this repository. For the backend, import the repository in Vercel and set the root directory to `backend`. Vercel detects FastAPI from `app/main.py` and uses Python 3.14 from `.python-version`. Check `GET /health` on the deployment URL. The first request after idle time can take a few seconds while the function starts.
