# coding=utf-8

from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Mapped

from app.db import Base

if TYPE_CHECKING:
    from ..models import Receipt


class PaymentMethod(Base):
    """
    Model of table for save payment-method

    Attributes:
        id (int): Unique identifier for the payment method.
        title (str): The name of the payment method.
        code (str): A unique identifier code for the payment method.

    Relationships:
        receipts (list[Receipt]): A list of receipts associated with a specific payment method.
    """

    __tablename__ = 'payment_method'

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, nullable=False)
    code = Column(String, unique=True, nullable=False)

    # Relationship to 'Receipt' table
    receipts: Mapped[list["Receipt"]] = relationship(
        "Receipt",
        back_populates="payment_method"
    )
