# coding=utf-8

import pytest
import pytest_asyncio
import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.db import Base, get_session
from app.conf import TEST_DATABASE_URL


# Test Database Configuration
TEST_ENGINE = create_async_engine(TEST_DATABASE_URL, echo=True)
TestingSessionLocal = async_sessionmaker(bind=TEST_ENGINE, expire_on_commit=False, class_=AsyncSession)


@pytest.fixture(scope="session")
def event_loop():
    """
    Creates a single event loop for the entire test session.
    Prevents conflicts between `event_loop` and `test_db`.
    """

    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_db():
    """
    Creates the test database once before running all tests.
    The database will be dropped only after the entire test session ends.
    """

    async with TEST_ENGINE.begin() as conn:
        # Clear the database before tests
        await conn.run_sync(Base.metadata.drop_all)

        # Create database schema
        await conn.run_sync(Base.metadata.create_all)

    yield  # Allow tests to use this database

    # Drop all data only after all tests are completed
    async with TEST_ENGINE.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db_session(test_db) -> AsyncSession:
    """
    Provides a database session for each test.
    The session commits changes between tests but does not delete records after each test.
    """

    async with TestingSessionLocal() as session:
        yield session

        # Ensure changes persist across tests
        await session.commit()
        await session.close()


@pytest_asyncio.fixture
async def override_get_session(db_session):
    """
    Overrides the default database session in FastAPI for testing.
    """
    async def get_test_db():
        async with db_session as session:
            yield session

    app.dependency_overrides[get_session] = get_test_db  # noqa
    yield
    app.dependency_overrides.clear()  # noqa


@pytest_asyncio.fixture
async def client(override_get_session) -> AsyncClient:
    """
    Provides an AsyncClient with the overridden test database.
    """
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as async_client:
        yield async_client
