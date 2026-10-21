from decimal import Decimal

import pytest
from fastapi.testclient import TestClient

from app.api.dependencies import get_insights_service
from app.main import app
from app.schemas.insights import GroupPayStats, InsightsParams, PayStats
from app.services.insights_service import InsightsService
from tests.fakes import FakeInsightsRepository

URL = "/api/v1/insights/summary"


def stats(median: str, headcount: int = 1) -> dict:
    value = Decimal(median)
    return {
        "headcount": headcount,
        "min": value,
        "p25": value,
        "median": value,
        "p75": value,
        "max": value,
        "average": value,
    }


@pytest.fixture
def service():
    groups = [
        GroupPayStats(key="FR", **stats("70000.00")),
        GroupPayStats(key="US", **stats("120000.00")),
        GroupPayStats(key="DE", **stats("70000.00")),
    ]
    return InsightsService(
        FakeInsightsRepository(PayStats(**stats("80000.00", headcount=3)), groups)
    )


@pytest.fixture
def client(service):
    app.dependency_overrides[get_insights_service] = lambda: service
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_groups_are_ordered_by_median_then_key(service):
    summary = service.summary(InsightsParams(group_by="country"))

    assert [group.key for group in summary.groups] == ["US", "DE", "FR"]


def test_summary_includes_overall_and_currency(service):
    summary = service.summary(InsightsParams(group_by="country"))

    assert summary.overall.headcount == 3
    assert summary.currency == "USD"
    assert summary.group_by == "country"


def test_endpoint_returns_money_as_strings(client):
    response = client.get(URL, params={"group_by": "country"})

    assert response.status_code == 200
    body = response.json()
    assert body["overall"]["median"] == "80000.00"
    assert body["groups"][0]["key"] == "US"
    assert body["groups"][0]["median"] == "120000.00"
    assert body["groups"][0]["headcount"] == 1


@pytest.mark.parametrize("params", [{}, {"group_by": "salary"}, {"group_by": "x"}])
def test_endpoint_requires_a_valid_group_by(client, params):
    assert client.get(URL, params=params).status_code == 422
