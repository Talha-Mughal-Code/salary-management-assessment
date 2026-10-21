import pytest
from sqlalchemy import func, select

from app.models import Employee
from app.scripts.seed import ExistingEmployeesError, seed_employees

pytestmark = pytest.mark.integration


def test_reset_replaces_all_employees(session):
    seed_employees(session, count=50, seed=1, reset=True)

    assert session.scalar(select(func.count()).select_from(Employee)) == 50


def test_refuses_to_seed_over_existing_employees(session):
    seed_employees(session, count=5, seed=1, reset=True)

    with pytest.raises(ExistingEmployeesError):
        seed_employees(session, count=5, seed=2, reset=False)
