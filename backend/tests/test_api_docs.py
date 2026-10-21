from fastapi.routing import APIRoute

from app.api.tags import TAGS_METADATA
from app.main import app

API_ROUTES = [route for route in app.routes if isinstance(route, APIRoute)]
DESCRIBED_TAGS = {tag["name"] for tag in TAGS_METADATA if tag.get("description")}


def test_every_route_has_a_described_tag():
    untagged = [
        route.path
        for route in API_ROUTES
        if not route.tags or not set(route.tags) <= DESCRIBED_TAGS
    ]

    assert untagged == []


def test_every_tag_has_a_description():
    assert DESCRIBED_TAGS == {tag["name"] for tag in TAGS_METADATA}


def test_every_route_has_a_summary_and_description():
    undocumented = [
        route.path for route in API_ROUTES if not route.summary or not route.description
    ]

    assert undocumented == []
