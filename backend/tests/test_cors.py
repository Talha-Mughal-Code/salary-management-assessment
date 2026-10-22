from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
ORIGIN = "https://frontend.example"


def test_preflight_allows_patch_with_json_from_any_origin():
    response = client.options(
        "/api/v1/employees/1",
        headers={
            "Origin": ORIGIN,
            "Access-Control-Request-Method": "PATCH",
            "Access-Control-Request-Headers": "content-type",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "*"
    assert "PATCH" in response.headers["access-control-allow-methods"]


def test_simple_request_gets_the_allow_origin_header():
    response = client.get("/health", headers={"Origin": ORIGIN})

    assert response.headers["access-control-allow-origin"] == "*"
    assert "access-control-allow-credentials" not in response.headers
