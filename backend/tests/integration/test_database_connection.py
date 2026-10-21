import pytest
from sqlalchemy import text

from app.core.database import get_session

pytestmark = pytest.mark.integration


def test_session_runs_a_query():
    session = next(get_session())

    assert session.execute(text("SELECT 1")).scalar_one() == 1
