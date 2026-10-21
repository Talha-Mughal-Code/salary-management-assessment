from collections.abc import Iterator
from functools import lru_cache

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import NullPool

from app.core.config import get_settings


@lru_cache
def get_engine() -> Engine:
    """No pool and no prepared statements: each serverless instance connects
    through Supabase's transaction pooler, which supports neither."""
    return create_engine(
        get_settings().database_url,
        poolclass=NullPool,
        connect_args={"prepare_threshold": None},
    )


def get_session() -> Iterator[Session]:
    with Session(get_engine()) as session:
        yield session
