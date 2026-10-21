import re
from datetime import timedelta

import pytest

from app.core.fx import to_usd
from app.scripts.seed import (
    HIRE_DATE_END,
    HIRE_WINDOW_DAYS,
    generate_employees,
)
from app.scripts.seed_data import COUNTRIES, US_BASE_SALARY_BY_TITLE

CURRENCY_BY_COUNTRY = {country.code: country.currency for country in COUNTRIES}
EMAIL_PATTERN = re.compile(r"^[a-z]+\.[a-z]+\d*@acme\.example$")


@pytest.fixture(scope="module")
def employees():
    return generate_employees(10_000, seed=42)


def test_same_seed_gives_same_employees():
    assert generate_employees(200, seed=7) == generate_employees(200, seed=7)


def test_different_seed_gives_different_employees():
    assert generate_employees(200, seed=7) != generate_employees(200, seed=8)


def test_generates_the_requested_count(employees):
    assert len(employees) == 10_000


def test_emails_are_unique_and_well_formed(employees):
    emails = [employee["email"] for employee in employees]

    assert len(set(emails)) == len(emails)
    assert all(EMAIL_PATTERN.match(email) for email in emails)


def test_currency_matches_country(employees):
    assert all(
        employee["currency"] == CURRENCY_BY_COUNTRY[employee["country"]]
        for employee in employees
    )


def test_every_country_is_present(employees):
    assert {employee["country"] for employee in employees} == set(CURRENCY_BY_COUNTRY)


def test_job_title_belongs_to_department(employees):
    assert all(
        employee["job_title"] in US_BASE_SALARY_BY_TITLE[employee["department"]]
        for employee in employees
    )


def test_salary_is_positive_and_converted_to_usd(employees):
    for employee in employees:
        assert employee["salary"] > 0
        assert employee["salary_usd"] == to_usd(
            employee["salary"], employee["currency"]
        )


def test_hire_dates_fall_in_the_window(employees):
    earliest = HIRE_DATE_END - timedelta(days=HIRE_WINDOW_DAYS)

    assert all(earliest <= e["hire_date"] <= HIRE_DATE_END for e in employees)
