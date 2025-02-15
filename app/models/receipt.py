# coding=utf-8

from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    Float,
    ForeignKey,
    String,
)
from sqlalchemy.orm import relationship, Mapped

from ..db import Base

if TYPE_CHECKING:
    from ..models import *


class Receipt(Base):
    """
    Model of table for save receipt

    Attributes:
        id (int): Unique identifier for the receipt.
        user_id (int): Foreign key to the user table, identifying the receipt creator.
        total (float): The total amount of the receipt (sum of all items).
        payment_type (str): The type of payment.
        payment_amount (float): The amount paid by the user.
        rest (float): The remaining balance to be refunded to the user.
        created_at (float): The timestamp when the receipt was created.

    Relationships:
        user (User): The user who created the receipt.
        items (list[ReceiptProduct]): The list of items associated with the receipt.
    """

    __tablename__ = 'receipt'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    total = Column(Float(10, 2), nullable=False)
    payment_type = Column(String, nullable=False)
    payment_amount = Column(Float(10, 2), nullable=False)
    rest = Column(Float(10, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship to 'User' table
    user: Mapped["User"] = relationship(
        "User",
        back_populates="receipts"
    )

    # Relationship to 'ReceiptProduct' table
    products: Mapped[list["ReceiptProduct"]] = relationship(
        "ReceiptProduct",
        back_populates="receipt"
    )
