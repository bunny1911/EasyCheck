# coding=utf-8

from typing import TYPE_CHECKING

from sqlalchemy.orm import relationship, Mapped
from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    ForeignKey
)

from ..db import Base

if TYPE_CHECKING:
    from ..models import Receipt


class ReceiptProduct(Base):
    """
    Model of table for save receipt-product

    Attributes:
        id (int): Unique identifier for the receipt item.
        receipt_id (int): Foreign key referencing the receipts table, identifying the associated receipt.
        title (str): The title of the product being purchased.
        price (float): The price of one unit of the product.
        quantity (int): The quantity of the product purchased.

    Relationships:
        receipt (Receipt): The associated receipt to which this item belongs.
    """

    __tablename__ = 'receipt_product'

    id = Column(Integer, primary_key=True, index=True)
    receipt_id = Column(Integer, ForeignKey('receipt.id'), nullable=False)
    title = Column(String, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False)

    # Relationship to 'Receipt' table
    receipt: Mapped["Receipt"] = relationship(
        "Receipt",
        back_populates="products"
    )

    @property
    def total(self) -> float:
        """
        Calculates the total price for a product by multiplying the unit price by the quantity.
        """

        return self.price * self.quantity
