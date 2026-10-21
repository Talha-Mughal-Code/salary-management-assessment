from sqlalchemy import Select, func, or_, select
from sqlalchemy.orm import Session

from app.models import Employee
from app.repositories.employee_filters import apply_employee_filters
from app.schemas.employee_list import EmployeeListParams, EmployeeQuery


class SqlAlchemyEmployeeRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def search(self, params: EmployeeListParams) -> tuple[list[Employee], int]:
        filtered = _apply_filters(select(Employee), params)
        total = self._session.scalar(
            select(func.count()).select_from(filtered.subquery())
        )
        page = (
            _apply_sort(filtered, params)
            .offset((params.page - 1) * params.page_size)
            .limit(params.page_size)
        )
        return list(self._session.scalars(page)), total or 0

    def all_matching(self, query: EmployeeQuery) -> list[Employee]:
        statement = _apply_sort(_apply_filters(select(Employee), query), query)
        return list(self._session.scalars(statement))

    def get(self, employee_id: int) -> Employee | None:
        return self._session.get(Employee, employee_id)

    def get_by_email(self, email: str) -> Employee | None:
        return self._session.scalar(select(Employee).where(Employee.email == email))

    def add(self, employee: Employee) -> Employee:
        self._session.add(employee)
        return self.save(employee)

    def save(self, employee: Employee) -> Employee:
        self._session.commit()
        self._session.refresh(employee)
        return employee

    def delete(self, employee: Employee) -> None:
        self._session.delete(employee)
        self._session.commit()


def _apply_sort(query: Select, params: EmployeeQuery) -> Select:
    column = getattr(Employee, params.sort)
    direction = column.desc() if params.order == "desc" else column.asc()
    return query.order_by(direction, Employee.id)


def _apply_filters(query: Select, params: EmployeeQuery) -> Select:
    if params.q:
        query = query.where(
            or_(
                Employee.full_name.icontains(params.q, autoescape=True),
                Employee.email.icontains(params.q, autoescape=True),
            )
        )
    return apply_employee_filters(query, params)
