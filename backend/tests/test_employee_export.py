import csv
import io
from datetime import UTC, date, datetime
from decimal import Decimal

from app.models import Employee
from app.services.employee_export import COLUMNS, employees_to_csv


def employee(full_name: str) -> Employee:
    now = datetime(2026, 10, 1, tzinfo=UTC)
    return Employee(
        id=7,
        full_name=full_name,
        email="x@acme.example",
        job_title="Analyst",
        department="Finance",
        country="FR",
        currency="EUR",
        salary=Decimal("50000.00"),
        salary_usd=Decimal("54000.00"),
        hire_date=date(2024, 1, 15),
        created_at=now,
        updated_at=now,
    )


def parse(text: str) -> list[dict]:
    return list(csv.DictReader(io.StringIO(text)))


def test_header_lists_every_column():
    assert employees_to_csv([]).splitlines() == [",".join(COLUMNS)]


def test_row_holds_plain_values():
    row = parse(employees_to_csv([employee("Chloé Martin")]))[0]

    assert row["full_name"] == "Chloé Martin"
    assert row["salary"] == "50000.00"
    assert row["salary_usd"] == "54000.00"
    assert row["hire_date"] == "2024-01-15"


def test_commas_and_quotes_are_escaped():
    row = parse(employees_to_csv([employee('Lee, "Danny"')]))[0]

    assert row["full_name"] == 'Lee, "Danny"'


def test_formula_like_text_is_neutralized():
    row = parse(employees_to_csv([employee('=HYPERLINK("http://x")')]))[0]

    assert row["full_name"] == '\'=HYPERLINK("http://x")'
