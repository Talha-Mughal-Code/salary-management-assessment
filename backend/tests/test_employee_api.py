import pytest
from fastapi.testclient import TestClient

from app.api.dependencies import get_employee_service
from app.main import app
from app.services.employee_service import EmployeeService
from tests.fakes import FakeEmployeeRepository

URL = "/api/v1/employees"
NEW_EMPLOYEE = {
    "full_name": "Anna Schmidt",
    "email": "Anna.Schmidt@acme.example",
    "job_title": "Software Engineer",
    "department": "Engineering",
    "country": "DE",
    "currency": "EUR",
    "salary": "60000.00",
    "hire_date": "2022-03-01",
}


@pytest.fixture
def client():
    service = EmployeeService(FakeEmployeeRepository())
    app.dependency_overrides[get_employee_service] = lambda: service
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_create_returns_201_with_computed_fields(client):
    response = client.post(URL, json=NEW_EMPLOYEE)

    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["email"] == "anna.schmidt@acme.example"
    assert body["salary_usd"] == "64800.00"


def test_create_with_invalid_body_returns_422(client):
    response = client.post(URL, json={**NEW_EMPLOYEE, "salary": "-1"})

    assert response.status_code == 422


def test_create_with_duplicate_email_returns_409(client):
    client.post(URL, json=NEW_EMPLOYEE)

    response = client.post(URL, json=NEW_EMPLOYEE)

    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]


def test_get_returns_the_employee(client):
    client.post(URL, json=NEW_EMPLOYEE)

    response = client.get(f"{URL}/1")

    assert response.status_code == 200
    assert response.json()["full_name"] == "Anna Schmidt"


def test_get_missing_employee_returns_404(client):
    response = client.get(f"{URL}/99")

    assert response.status_code == 404
    assert response.json() == {"detail": "Employee 99 not found"}


def test_patch_updates_salary_and_usd(client):
    client.post(URL, json=NEW_EMPLOYEE)

    response = client.patch(f"{URL}/1", json={"salary": "70000.00"})

    assert response.status_code == 200
    assert response.json()["salary_usd"] == "75600.00"


def test_patch_with_null_returns_422(client):
    client.post(URL, json=NEW_EMPLOYEE)

    response = client.patch(f"{URL}/1", json={"department": None})

    assert response.status_code == 422


def test_patch_missing_employee_returns_404(client):
    response = client.patch(f"{URL}/99", json={"salary": "1.00"})

    assert response.status_code == 404


def test_delete_returns_204_and_removes_employee(client):
    client.post(URL, json=NEW_EMPLOYEE)

    response = client.delete(f"{URL}/1")

    assert response.status_code == 204
    assert client.get(f"{URL}/1").status_code == 404


def test_delete_missing_employee_returns_404(client):
    assert client.delete(f"{URL}/99").status_code == 404
