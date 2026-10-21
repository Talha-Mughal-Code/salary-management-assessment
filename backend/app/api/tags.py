HEALTH = "health"
EMPLOYEES = "employees"
INSIGHTS = "insights"

TAGS_METADATA = [
    {"name": HEALTH, "description": "Liveness check used by the hosting platform."},
    {
        "name": EMPLOYEES,
        "description": "Create, read, update and delete employees. "
        "Salaries are in local currency; `salary_usd` is computed by the server.",
    },
    {
        "name": INSIGHTS,
        "description": "How ACME pays people: salary statistics in USD, "
        "computed in the database with the same filters as the employee list.",
    },
]
