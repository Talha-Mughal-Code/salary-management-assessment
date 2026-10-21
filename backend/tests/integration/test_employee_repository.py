from datetime import date
from decimal import Decimal

import pytest

from app.models import Employee
from app.repositories.sqlalchemy_employee_repository import (
    SqlAlchemyEmployeeRepository,
)

pytestmark = pytest.mark.integration


def new_employee() -> Employee:
    return Employee(
        full_name="Repo Test",
        email="repo.test@acme.example",
        job_title="Accountant",
        department="Finance",
        country="FR",
        currency="EUR",
        salary=Decimal("50000.00"),
        salary_usd=Decimal("54000.00"),
        hire_date=date(2024, 1, 15),
    )


def test_add_assigns_id_and_timestamps(session):
    employee = SqlAlchemyEmployeeRepository(session).add(new_employee())

    assert employee.id is not None
    assert employee.created_at is not None


def test_get_and_get_by_email_find_the_employee(session):
    repository = SqlAlchemyEmployeeRepository(session)
    employee = repository.add(new_employee())

    assert repository.get(employee.id) is employee
    assert repository.get_by_email("repo.test@acme.example") is employee


def test_save_persists_changes(session):
    repository = SqlAlchemyEmployeeRepository(session)
    employee = repository.add(new_employee())

    employee.job_title = "Financial Analyst"
    repository.save(employee)
    session.expire_all()

    assert repository.get(employee.id).job_title == "Financial Analyst"


def test_delete_removes_the_employee(session):
    repository = SqlAlchemyEmployeeRepository(session)
    employee = repository.add(new_employee())

    repository.delete(employee)

    assert repository.get(employee.id) is None
