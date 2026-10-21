from collections import Counter
from datetime import UTC, datetime
from decimal import Decimal

from app.models import Employee
from app.schemas.employee_list import EmployeeListParams
from app.schemas.insights import (
    GroupPayStats,
    InsightsFilters,
    InsightsParams,
    PayStats,
)


class FakeEmployeeRepository:
    def __init__(self) -> None:
        self.employees: dict[int, Employee] = {}
        self._next_id = 1

    def search(self, params: EmployeeListParams) -> tuple[list[Employee], int]:
        matches = sorted(
            (e for e in self.employees.values() if _matches(e, params)),
            key=lambda e: e.id,
        )
        matches.sort(
            key=lambda e: getattr(e, params.sort), reverse=params.order == "desc"
        )
        start = (params.page - 1) * params.page_size
        return matches[start : start + params.page_size], len(matches)

    def get(self, employee_id: int) -> Employee | None:
        return self.employees.get(employee_id)

    def get_by_email(self, email: str) -> Employee | None:
        return next((e for e in self.employees.values() if e.email == email), None)

    def add(self, employee: Employee) -> Employee:
        employee.id = self._next_id
        employee.created_at = datetime.now(UTC)
        self._next_id += 1
        self.employees[employee.id] = employee
        return self.save(employee)

    def save(self, employee: Employee) -> Employee:
        employee.updated_at = datetime.now(UTC)
        return employee

    def delete(self, employee: Employee) -> None:
        del self.employees[employee.id]


def _matches(employee: Employee, params: EmployeeListParams) -> bool:
    text = f"{employee.full_name} {employee.email}".lower()
    return (
        (not params.q or params.q.lower() in text)
        and (not params.country or employee.country == params.country)
        and (not params.job_title or employee.job_title == params.job_title)
        and (not params.department or employee.department == params.department)
    )


class FakeInsightsRepository:
    def __init__(
        self,
        overall: PayStats | None = None,
        groups: list[GroupPayStats] | None = None,
        salaries: list[Decimal] | None = None,
    ) -> None:
        self._overall = overall
        self._groups = groups or []
        self._salaries = salaries or []

    def overall(self, params: InsightsParams) -> PayStats | None:
        return self._overall

    def by_group(self, params: InsightsParams) -> list[GroupPayStats]:
        return list(self._groups)

    def salary_range(self, filters: InsightsFilters) -> tuple[Decimal, Decimal] | None:
        if not self._salaries:
            return None
        return min(self._salaries), max(self._salaries)

    def bucket_counts(
        self, filters: InsightsFilters, start: Decimal, width: Decimal
    ) -> dict[int, int]:
        return dict(Counter(int((s - start) // width) for s in self._salaries))
