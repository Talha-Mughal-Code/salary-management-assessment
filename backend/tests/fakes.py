from app.models import Employee


class FakeEmployeeRepository:
    def __init__(self) -> None:
        self.employees: dict[int, Employee] = {}
        self._next_id = 1

    def get(self, employee_id: int) -> Employee | None:
        return self.employees.get(employee_id)

    def get_by_email(self, email: str) -> Employee | None:
        return next((e for e in self.employees.values() if e.email == email), None)

    def add(self, employee: Employee) -> Employee:
        employee.id = self._next_id
        self._next_id += 1
        self.employees[employee.id] = employee
        return employee

    def save(self, employee: Employee) -> Employee:
        return employee

    def delete(self, employee: Employee) -> None:
        del self.employees[employee.id]
