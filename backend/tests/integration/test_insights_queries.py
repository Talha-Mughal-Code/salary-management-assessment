from datetime import date
from decimal import Decimal

import pytest
from sqlalchemy import delete

from app.models import Employee
from app.repositories.sqlalchemy_insights_repository import (
    SqlAlchemyInsightsRepository,
)
from app.schemas.insights import InsightsFilters, InsightsParams

pytestmark = pytest.mark.integration

ROWS = [
    ("DE", "Engineering", "10000.00"),
    ("DE", "Engineering", "20000.00"),
    ("DE", "Finance", "30000.00"),
    ("DE", "Finance", "40000.00"),
    ("US", "Engineering", "100000.00"),
]


@pytest.fixture
def repository(session):
    session.execute(delete(Employee))
    for index, (country, department, salary_usd) in enumerate(ROWS):
        session.add(
            Employee(
                full_name=f"Person {index}",
                email=f"person{index}@acme.example",
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
    return SqlAlchemyInsightsRepository(session)


def test_overall_stats_match_hand_computed_values(repository):
    overall = repository.overall(InsightsParams(group_by="country"))

    assert overall.model_dump() == {
        "headcount": 5,
        "min": Decimal("10000.00"),
        "p25": Decimal("20000.00"),
        "median": Decimal("30000.00"),
        "p75": Decimal("40000.00"),
        "max": Decimal("100000.00"),
        "average": Decimal("40000.00"),
    }


def test_percentiles_interpolate_between_rows(repository):
    groups = {
        group.key: group
        for group in repository.by_group(InsightsParams(group_by="country"))
    }

    assert groups["DE"].headcount == 4
    assert groups["DE"].p25 == Decimal("17500.00")
    assert groups["DE"].median == Decimal("25000.00")
    assert groups["DE"].p75 == Decimal("32500.00")
    assert groups["US"].median == Decimal("100000.00")


def test_filters_apply_before_grouping(repository):
    params = InsightsParams(group_by="department", country="DE")

    groups = {group.key: group.median for group in repository.by_group(params)}

    assert groups == {
        "Engineering": Decimal("15000.00"),
        "Finance": Decimal("35000.00"),
    }


def test_no_matching_employees_gives_empty_stats(repository):
    params = InsightsParams(group_by="country", country="JP")

    assert repository.overall(params).headcount == 0
    assert repository.overall(params).median is None
    assert repository.by_group(params) == []


def test_salary_range_and_bucket_counts(repository):
    filters = InsightsFilters(country="DE")

    assert repository.salary_range(filters) == (
        Decimal("10000.00"),
        Decimal("40000.00"),
    )
    assert repository.bucket_counts(filters, Decimal("10000"), Decimal("15000")) == {
        0: 2,
        1: 1,
        2: 1,
    }


def test_salary_range_is_none_without_employees(repository):
    assert repository.salary_range(InsightsFilters(country="JP")) is None
