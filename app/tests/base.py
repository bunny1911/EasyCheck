# coding=utf-8

from pathlib import Path
from typing import Generator

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from ..main import app
from ..db import Base, get_session
from ..conf import DATABASE_URL, TEST_DATABASE_URL
from .funcs import *


# Admin connection (for DB creation/deletion)
admin_db_engine = create_sync_engine(DATABASE_URL, autocommit=True)

# Synchronous engine for tests
test_db_engine = create_sync_engine(TEST_DATABASE_URL)

# Asynchronous engine for test sessions
test_db_async_engine = create_async_engine_instance(TEST_DATABASE_URL)

# Defined testing session-local
TestingSessionLocal = sessionmaker(
    autocommit=False,
    class_=AsyncSession,
    autoflush=False,
    bind=test_db_async_engine
)


def create_test_database():
    """
    Create new test database or clear it if exists
    """

    with admin_db_engine.connect() as connection:
        # If exists, drop database
        connection.execute(
            text(f"DROP DATABASE IF EXISTS {TEST_DATABASE_URL.split('/')[-1]}")
        )

        # Create new database
        connection.execute(
            text(f"CREATE DATABASE {TEST_DATABASE_URL.split('/')[-1]}")
        )

    # Now we need to run migrations
    alembic_cfg = Config()
    alembic_cfg.set_main_option("script_location", str(Path().absolute().parent / "migrations"))
    alembic_cfg.set_main_option("sqlalchemy.url", TEST_DATABASE_URL)
    command.upgrade(alembic_cfg, "head")


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """
    Create the test database schema before any tests run,
    and drop it after all tests are done.
    """

    # Ensure the test database is created
    create_test_database()

    # Create tables
    Base.metadata.create_all(bind=test_db_engine)
    yield

    # Drop tables after tests
    Base.metadata.drop_all(bind=test_db_engine)


@pytest.fixture(scope="function")
def client() -> Generator[TestClient, None, None]:
    """
    Provide a TestClient that uses the test database session.
    Override the get_db dependency to use the test session.
    """

    async def override_get_db():
        async with TestingSessionLocal(bind=test_db_async_engine) as db:
            yield db

    app.dependency_overrides[get_session] = override_get_db  # noqa
    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear() # noqa
