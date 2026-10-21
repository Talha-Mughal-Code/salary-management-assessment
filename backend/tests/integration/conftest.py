import pytest
from sqlalchemy.orm import Session

from app.core.database import get_engine


@pytest.fixture
def session():
    """Commits inside a test land in a savepoint that is rolled back afterwards."""
    with get_engine().connect() as connection:
        transaction = connection.begin()
        with Session(bind=connection, join_transaction_mode="create_savepoint") as s:
            yield s
        transaction.rollback()
