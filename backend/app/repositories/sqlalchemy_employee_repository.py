from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Employee


class SqlAlchemyEmployeeRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

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
