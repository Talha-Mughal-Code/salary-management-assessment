from decimal import Decimal

import pytest

from app.schemas.employee import EmployeeCreate, EmployeeUpdate
from app.schemas.employee_list import EmployeeListParams
from app.services.employee_service import EmployeeService
from app.services.errors import DuplicateEmailError, EmployeeNotFoundError
from tests.fakes import FakeEmployeeRepository


def new_employee(**overrides) -> EmployeeCreate:
    fields = {
        "full_name": "Anna Schmidt",
        "email": "Anna.Schmidt@acme.example",
        "job_title": "Software Engineer",
        "department": "Engineering",
        "country": "DE",
        "currency": "EUR",
        "salary": "60000.00",
        "hire_date": "2022-03-01",
    }
    return EmployeeCreate.model_validate({**fields, **overrides})


@pytest.fixture
def repository():
    return FakeEmployeeRepository()


@pytest.fixture
def service(repository):
    return EmployeeService(repository)


def test_create_lowercases_email_and_computes_usd(service):
    employee = service.create(new_employee())

    assert employee.id == 1
    assert employee.email == "anna.schmidt@acme.example"
    assert employee.salary_usd == Decimal("64800.00")


def test_create_rejects_duplicate_email_in_any_case(service):
    service.create(new_employee())

    with pytest.raises(DuplicateEmailError):
        service.create(new_employee(email="ANNA.SCHMIDT@acme.example"))


def test_get_missing_employee_raises(service):
    with pytest.raises(EmployeeNotFoundError):
        service.get(99)


def test_update_salary_recomputes_usd(service):
    employee = service.create(new_employee())

    updated = service.update(employee.id, EmployeeUpdate(salary="70000.00"))

    assert updated.salary == Decimal("70000.00")
    assert updated.salary_usd == Decimal("75600.00")


def test_update_currency_recomputes_usd(service):
    employee = service.create(new_employee())

    updated = service.update(employee.id, EmployeeUpdate(currency="GBP"))

    assert updated.salary_usd == Decimal("76200.00")


def test_update_changes_only_given_fields(service):
    employee = service.create(new_employee())

    updated = service.update(employee.id, EmployeeUpdate(job_title="Staff Engineer"))

    assert updated.job_title == "Staff Engineer"
    assert updated.department == "Engineering"
    assert updated.salary == Decimal("60000.00")


def test_update_to_another_employees_email_is_rejected(service):
    service.create(new_employee())
    other = service.create(new_employee(email="ben@acme.example"))

    with pytest.raises(DuplicateEmailError):
        service.update(other.id, EmployeeUpdate(email="anna.schmidt@acme.example"))


def test_update_own_email_in_another_case_is_allowed(service):
    employee = service.create(new_employee())

    updated = service.update(
        employee.id, EmployeeUpdate(email="ANNA.SCHMIDT@acme.example")
    )

    assert updated.email == "anna.schmidt@acme.example"


def test_update_missing_employee_raises(service):
    with pytest.raises(EmployeeNotFoundError):
        service.update(99, EmployeeUpdate(salary="1.00"))


def test_delete_removes_employee(service, repository):
    employee = service.create(new_employee())

    service.delete(employee.id)

    assert repository.employees == {}


def test_delete_missing_employee_raises(service):
    with pytest.raises(EmployeeNotFoundError):
        service.delete(99)


def test_search_wraps_results_in_a_page(service):
    service.create(new_employee())

    page = service.search(EmployeeListParams(page_size=10))

    assert (page.total, page.page, page.page_size) == (1, 1, 10)
    assert page.items[0].email == "anna.schmidt@acme.example"
