from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.repositories.sqlalchemy_employee_repository import (
    SqlAlchemyEmployeeRepository,
)
from app.services.employee_service import EmployeeService


def get_employee_service(
    session: Annotated[Session, Depends(get_session)],
) -> EmployeeService:
    return EmployeeService(SqlAlchemyEmployeeRepository(session))


EmployeeServiceDep = Annotated[EmployeeService, Depends(get_employee_service)]
