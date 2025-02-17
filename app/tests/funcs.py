# coding=utf-8

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine


def create_sync_engine(database_url: str, autocommit: bool = False):
    """
    Create a synchronous SQLAlchemy engine.
    """
    return create_engine(
        database_url.replace("+asyncpg", ""),
        isolation_level="AUTOCOMMIT"
        if autocommit else None
    )


def create_async_engine_instance(database_url: str):
    """
    Create an asynchronous SQLAlchemy engine.
    """

    return create_async_engine(database_url)
