class EmployeeNotFoundError(Exception):
    def __init__(self, employee_id: int) -> None:
        super().__init__(f"Employee {employee_id} not found")
        self.employee_id = employee_id


class DuplicateEmailError(Exception):
    def __init__(self, email: str) -> None:
        super().__init__(f"An employee with email {email} already exists")
        self.email = email
