import csv
import io
from collections.abc import Iterable

from app.models import Employee

COLUMNS = (
    "id",
    "full_name",
    "email",
    "job_title",
    "department",
    "country",
    "currency",
    "salary",
    "salary_usd",
    "hire_date",
    "created_at",
    "updated_at",
)
FORMULA_PREFIXES = ("=", "+", "-", "@", "\t", "\r")


def employees_to_csv(employees: Iterable[Employee]) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(COLUMNS)
    for employee in employees:
        writer.writerow(_cell(getattr(employee, column)) for column in COLUMNS)
    return buffer.getvalue()


def _cell(value: object) -> object:
    """Text starting with a formula character is prefixed so spreadsheets
    show it as text instead of running it."""
    if isinstance(value, str) and value.startswith(FORMULA_PREFIXES):
        return f"'{value}"
    return value
