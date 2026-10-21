import pytest
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.database import get_engine
from app.models import Employee
from app.scripts.seed import ExistingEmployeesError, seed_employees

pytestmark = pytest.mark.integration


@pytest.fixture
def session():
    with Session(get_engine()) as session:
        yield session
        session.rollback()


def test_reset_replaces_all_employees(session):
    seed_employees(session, count=50, seed=1, reset=True)

    assert session.scalar(select(func.count()).select_from(Employee)) == 50


def test_refuses_to_seed_over_existing_employees(session):
    seed_employees(session, count=5, seed=1, reset=True)

    with pytest.raises(ExistingEmployeesError):
        seed_employees(session, count=5, seed=2, reset=False)
