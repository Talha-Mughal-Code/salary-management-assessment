from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.repositories.sqlalchemy_employee_repository import (
    SqlAlchemyEmployeeRepository,
)
from app.repositories.sqlalchemy_insights_repository import (
    SqlAlchemyInsightsRepository,
)
from app.services.employee_service import EmployeeService
from app.services.insights_service import InsightsService


def get_employee_service(
    session: Annotated[Session, Depends(get_session)],
) -> EmployeeService:
    return EmployeeService(SqlAlchemyEmployeeRepository(session))


def get_insights_service(
    session: Annotated[Session, Depends(get_session)],
) -> InsightsService:
    return InsightsService(SqlAlchemyInsightsRepository(session))


EmployeeServiceDep = Annotated[EmployeeService, Depends(get_employee_service)]
InsightsServiceDep = Annotated[InsightsService, Depends(get_insights_service)]
