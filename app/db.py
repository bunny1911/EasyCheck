# coding=utf-8

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from .conf import DATABASE_URL

# Connect to DB
engine = create_engine(DATABASE_URL)

# Defined session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Defined base model class
Base = declarative_base()


def get_session() -> Session:
    """
    Returns a new session to interact with the database.
    """

    # Create a new session
    db = SessionLocal()

    try:
        # Provide session to the route or operation
        yield db

    finally:
        # Ensure the session is closed when done
        db.close()
