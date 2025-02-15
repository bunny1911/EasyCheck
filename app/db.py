# coding=utf-8

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from .conf import DATABASE_URL

# Connect to DB
engine = create_async_engine(DATABASE_URL, echo=True)

# Defined session
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
)

# Defined base model class
Base = declarative_base()


async def get_session():
    """
    Generates a new database session for each request.
    """

    async with SessionLocal() as session:
        yield session
