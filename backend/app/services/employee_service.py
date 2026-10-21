from app.core.fx import to_usd
from app.models import Employee
from app.repositories.employee_repository import EmployeeRepository
from app.schemas.employee import EmployeeCreate, EmployeeUpdate
from app.services.errors import DuplicateEmailError, EmployeeNotFoundError


class EmployeeService:
    def __init__(self, repository: EmployeeRepository) -> None:
        self._repository = repository

    def create(self, data: EmployeeCreate) -> Employee:
        fields = data.model_dump()
        fields["email"] = fields["email"].lower()
        self._ensure_email_is_free(fields["email"])
        employee = Employee(**fields, salary_usd=to_usd(data.salary, data.currency))
        return self._repository.add(employee)

    def get(self, employee_id: int) -> Employee:
        employee = self._repository.get(employee_id)
        if employee is None:
            raise EmployeeNotFoundError(employee_id)
        return employee

    def update(self, employee_id: int, data: EmployeeUpdate) -> Employee:
        employee = self.get(employee_id)
        changes = data.model_dump(exclude_unset=True)
        if "email" in changes:
            changes["email"] = changes["email"].lower()
            if changes["email"] != employee.email:
                self._ensure_email_is_free(changes["email"])

        for field, value in changes.items():
            setattr(employee, field, value)
        employee.salary_usd = to_usd(employee.salary, employee.currency)
        return self._repository.save(employee)

    def delete(self, employee_id: int) -> None:
        self._repository.delete(self.get(employee_id))

    def _ensure_email_is_free(self, email: str) -> None:
        if self._repository.get_by_email(email) is not None:
            raise DuplicateEmailError(email)
