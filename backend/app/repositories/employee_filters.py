from typing import Protocol

from sqlalchemy import Select

from app.models import Employee


class EmployeeFilters(Protocol):
    country: str | None
    job_title: str | None
    department: str | None


def apply_employee_filters(query: Select, filters: EmployeeFilters) -> Select:
    if filters.country:
        query = query.where(Employee.country == filters.country)
    if filters.job_title:
        query = query.where(Employee.job_title == filters.job_title)
    if filters.department:
        query = query.where(Employee.department == filters.department)
    return query
