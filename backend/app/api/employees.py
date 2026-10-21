from fastapi import APIRouter, status

from app.api.dependencies import EmployeeServiceDep
from app.api.errors import DUPLICATE_EMAIL_RESPONSE, NOT_FOUND_RESPONSE
from app.api.tags import EMPLOYEES
from app.models import Employee
from app.schemas.employee import EmployeeCreate, EmployeeResponse, EmployeeUpdate

router = APIRouter(prefix="/api/v1/employees", tags=[EMPLOYEES])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Create an employee",
    description="Adds an employee. The email is stored in lowercase and must be "
    "unique. `salary_usd` is computed from the fixed exchange rates.",
    response_model=EmployeeResponse,
    responses=DUPLICATE_EMAIL_RESPONSE,
)
def create_employee(data: EmployeeCreate, service: EmployeeServiceDep) -> Employee:
    return service.create(data)


@router.get(
    "/{employee_id}",
    summary="Get an employee",
    description="Returns one employee by id.",
    response_model=EmployeeResponse,
    responses=NOT_FOUND_RESPONSE,
)
def get_employee(employee_id: int, service: EmployeeServiceDep) -> Employee:
    return service.get(employee_id)


@router.patch(
    "/{employee_id}",
    summary="Update an employee",
    description="Changes only the fields sent. `salary_usd` is recomputed.",
    response_model=EmployeeResponse,
    responses={**NOT_FOUND_RESPONSE, **DUPLICATE_EMAIL_RESPONSE},
)
def update_employee(
    employee_id: int, data: EmployeeUpdate, service: EmployeeServiceDep
) -> Employee:
    return service.update(employee_id, data)


@router.delete(
    "/{employee_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an employee",
    description="Permanently removes the employee.",
    response_model=None,
    responses=NOT_FOUND_RESPONSE,
)
def delete_employee(employee_id: int, service: EmployeeServiceDep) -> None:
    service.delete(employee_id)
