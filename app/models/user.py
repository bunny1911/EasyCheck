# coding=utf-8

from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy.orm import relationship, Mapped
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
)

from ..db import Base

if TYPE_CHECKING:
    from ..models import Receipt


class User(Base):
    """
    Model of table for save user

    Attributes:
        id (int): The unique identifier for the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        login (str): The login username, must be unique.
        hashed_password (str): The hashed password for secure authentication.
        created_at (datetime): The timestamp when the user account was created.

    Relationships:
        receipts (list["Receipt"]): A list of receipts associated with the user.
    """

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    login = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship to 'Receipt' table
    receipts: Mapped[list["Receipt"]] = relationship(
        "Receipt",
        back_populates="user"
    )
