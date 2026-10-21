HEALTH = "health"
EMPLOYEES = "employees"

TAGS_METADATA = [
    {"name": HEALTH, "description": "Liveness check used by the hosting platform."},
    {
        "name": EMPLOYEES,
        "description": "Create, read, update and delete employees. "
        "Salaries are in local currency; `salary_usd` is computed by the server.",
    },
]
