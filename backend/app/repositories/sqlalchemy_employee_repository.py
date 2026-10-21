from sqlalchemy import Select, func, or_, select
from sqlalchemy.orm import Session

from app.models import Employee
from app.schemas.employee_list import EmployeeListParams


class SqlAlchemyEmployeeRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def search(self, params: EmployeeListParams) -> tuple[list[Employee], int]:
        filtered = _apply_filters(select(Employee), params)
        total = self._session.scalar(
            select(func.count()).select_from(filtered.subquery())
        )
        sort_column = getattr(Employee, params.sort)
        sort = sort_column.desc() if params.order == "desc" else sort_column.asc()
        page = (
            filtered.order_by(sort, Employee.id)
            .offset((params.page - 1) * params.page_size)
            .limit(params.page_size)
        )
        return list(self._session.scalars(page)), total or 0

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


def _apply_filters(query: Select, params: EmployeeListParams) -> Select:
    if params.q:
        query = query.where(
            or_(
                Employee.full_name.icontains(params.q, autoescape=True),
                Employee.email.icontains(params.q, autoescape=True),
            )
        )
    if params.country:
        query = query.where(Employee.country == params.country)
    if params.job_title:
        query = query.where(Employee.job_title == params.job_title)
    if params.department:
        query = query.where(Employee.department == params.department)
    return query
