from decimal import Decimal

import pytest
from fastapi.testclient import TestClient

from app.api.dependencies import get_insights_service
from app.main import app
from app.schemas.insights import InsightsFilters
from app.services.insights_service import InsightsService, nice_width
from tests.fakes import FakeInsightsRepository

URL = "/api/v1/insights/distribution"


def distribution(*salaries: str):
    repository = FakeInsightsRepository(salaries=[Decimal(s) for s in salaries])
    return InsightsService(repository).distribution(InsightsFilters())


@pytest.mark.parametrize(
    ("raw", "width"),
    [
        ("4499.95", "5000"),
        ("2100", "2500"),
        ("1000", "1000"),
        ("1001", "2000"),
        ("0", "1"),
    ],
)
def test_nice_width_rounds_up_to_a_round_number(raw, width):
    assert nice_width(Decimal(raw)) == Decimal(width)


def test_buckets_start_on_a_round_edge_and_cover_the_maximum():
    buckets = distribution("10000.00", "12500.00", "99999.00").buckets

    assert len(buckets) == 18
    assert (buckets[0].min, buckets[0].max, buckets[0].count) == (
        Decimal("10000.00"),
        Decimal("15000.00"),
        2,
    )
    assert (buckets[-1].min, buckets[-1].max, buckets[-1].count) == (
        Decimal("95000.00"),
        Decimal("100000.00"),
        1,
    )
    assert sum(bucket.count for bucket in buckets) == 3


def test_empty_buckets_are_included_with_zero():
    buckets = distribution("10000.00", "99999.00").buckets

    assert [bucket.count for bucket in buckets[1:-1]] == [0] * 16


def test_single_salary_gives_one_bucket():
    buckets = distribution("50000.00").buckets

    assert [(b.min, b.max, b.count) for b in buckets] == [
        (Decimal("50000.00"), Decimal("50001.00"), 1)
    ]


def test_no_employees_gives_no_buckets():
    assert distribution().buckets == []


def test_endpoint_returns_money_as_plain_strings():
    service = InsightsService(
        FakeInsightsRepository(salaries=[Decimal("10000.00"), Decimal("99999.00")])
    )
    app.dependency_overrides[get_insights_service] = lambda: service
    try:
        body = TestClient(app).get(URL, params={"country": "de"}).json()
    finally:
        app.dependency_overrides.clear()

    assert body["currency"] == "USD"
    assert body["buckets"][0] == {"min": "10000.00", "max": "15000.00", "count": 1}
