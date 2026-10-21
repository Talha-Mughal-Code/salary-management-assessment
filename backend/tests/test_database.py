import pytest
from sqlalchemy.pool import NullPool

from app.core.config import Settings, get_settings
from app.core.database import get_engine

DATABASE_URL = "postgresql+psycopg://user:secret@db.example:6543/app"


@pytest.fixture
def database_url_env(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", DATABASE_URL)
    get_settings.cache_clear()
    get_engine.cache_clear()
    yield
    get_settings.cache_clear()
    get_engine.cache_clear()


def test_settings_read_database_url_from_environment(database_url_env):
    assert Settings(_env_file=None).database_url == DATABASE_URL


def test_engine_disables_pooling_for_serverless(database_url_env):
    assert isinstance(get_engine().pool, NullPool)
