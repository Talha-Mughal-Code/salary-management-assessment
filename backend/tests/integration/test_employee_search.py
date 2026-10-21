from datetime import date
from decimal import Decimal

import pytest
from sqlalchemy import delete

from app.models import Employee
from app.repositories.sqlalchemy_employee_repository import (
    SqlAlchemyEmployeeRepository,
)
from app.schemas.employee_list import EmployeeListParams

pytestmark = pytest.mark.integration

ROWS = [
    ("Anna Schmidt", "anna@acme.example", "Engineering", "DE", "90000.00"),
    ("Ben Miller", "ben@acme.example", "Engineering", "US", "120000.00"),
    ("Chloé Martin", "chloe@acme.example", "Finance", "FR", "70000.00"),
    ("Dan 100% Lee", "dan@acme.example", "Finance", "US", "70000.00"),
]


@pytest.fixture
def repository(session):
    session.execute(delete(Employee))
    for name, email, department, country, salary_usd in ROWS:
        session.add(
            Employee(
                full_name=name,
                email=email,
                job_title="Analyst",
                department=department,
                country=country,
                currency="USD",
                salary=Decimal(salary_usd),
                salary_usd=Decimal(salary_usd),
                hire_date=date(2024, 1, 1),
            )
        )
    session.flush()
    return SqlAlchemyEmployeeRepository(session)


def names(repository, **params) -> tuple[list[str], int]:
    items, total = repository.search(EmployeeListParams(**params))
    return [employee.full_name for employee in items], total


def test_pages_are_ordered_and_counted(repository):
    assert names(repository, page=2, page_size=3) == (["Dan 100% Lee"], 4)


def test_page_past_the_end_is_empty_with_total(repository):
    assert names(repository, page=5, page_size=3) == ([], 4)


def test_q_matches_name_or_email_ignoring_case(repository):
    assert names(repository, q="SCHMIDT")[0] == ["Anna Schmidt"]
    assert names(repository, q="ben@")[0] == ["Ben Miller"]


def test_q_treats_percent_as_text(repository):
    assert names(repository, q="%")[0] == ["Dan 100% Lee"]


def test_filters_combine(repository):
    assert names(repository, department="Finance", country="US")[0] == ["Dan 100% Lee"]


def test_sort_by_salary_desc_breaks_ties_by_id(repository):
    assert names(repository, sort="salary_usd", order="desc")[0] == [
        "Ben Miller",
        "Anna Schmidt",
        "Chloé Martin",
        "Dan 100% Lee",
    ]
