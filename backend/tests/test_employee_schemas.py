from datetime import UTC, date, datetime
from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.schemas.employee import EmployeeCreate, EmployeeResponse, EmployeeUpdate

VALID = {
    "full_name": "  Anna Schmidt ",
    "email": "Anna.Schmidt@acme.example",
    "job_title": "Software Engineer",
    "department": "Engineering",
    "country": "de",
    "currency": "eur",
    "salary": "72000.00",
    "hire_date": "2022-03-01",
}


def error_fields(error: ValidationError) -> set[str]:
    return {".".join(str(part) for part in item["loc"]) for item in error.errors()}


def test_valid_input_is_normalized():
    employee = EmployeeCreate.model_validate(VALID)

    assert employee.full_name == "Anna Schmidt"
    assert employee.country == "DE"
    assert employee.currency == "EUR"
    assert employee.salary == Decimal("72000.00")
    assert employee.hire_date == date(2022, 3, 1)


def test_missing_field_is_rejected():
    payload = {key: value for key, value in VALID.items() if key != "job_title"}

    with pytest.raises(ValidationError) as error:
        EmployeeCreate.model_validate(payload)

    assert error_fields(error.value) == {"job_title"}


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("salary", "0"),
        ("salary", "-100"),
        ("salary", "100.555"),
        ("salary", "12345678901.00"),
        ("currency", "XYZ"),
        ("country", "DEU"),
        ("email", "not-an-email"),
        ("full_name", "   "),
    ],
)
def test_invalid_value_is_rejected(field, value):
    with pytest.raises(ValidationError) as error:
        EmployeeCreate.model_validate({**VALID, field: value})

    assert error_fields(error.value) == {field}


def test_unknown_field_is_rejected():
    with pytest.raises(ValidationError) as error:
        EmployeeCreate.model_validate({**VALID, "salary_usd": "1"})

    assert error_fields(error.value) == {"salary_usd"}


def test_empty_update_is_valid():
    assert EmployeeUpdate.model_validate({}).model_dump(exclude_unset=True) == {}


def test_update_applies_the_same_rules():
    with pytest.raises(ValidationError) as error:
        EmployeeUpdate.model_validate({"salary": "0"})

    assert error_fields(error.value) == {"salary"}


def test_update_rejects_null():
    with pytest.raises(ValidationError) as error:
        EmployeeUpdate.model_validate({"department": None})

    assert error_fields(error.value) == {"department"}


def test_response_returns_money_as_strings():
    now = datetime(2026, 10, 1, tzinfo=UTC)
    response = EmployeeResponse(
        id=1,
        **{key: value for key, value in VALID.items() if key != "salary"},
        salary=Decimal("72000.00"),
        salary_usd=Decimal("77760.00"),
        created_at=now,
        updated_at=now,
    )

    body = response.model_dump(mode="json")

    assert body["salary"] == "72000.00"
    assert body["salary_usd"] == "77760.00"
