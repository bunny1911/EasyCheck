from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class ReceiptItemSchema(BaseModel):
    title: str = Field(
        ...,
        example="Product Name",
        description="The name of the product/item included in the receipt."
    )
    price: float = Field(
        ...,
        example=99.99,
        description="The price per unit of the product/item."
    )
    quantity: float = Field(
        ...,
        example=2.5,
        description="The quantity or weight of the product/item purchased."
    )

    class Config:
        orm_mode = True


class ReceiptPaymentSchema(BaseModel):
    type: str = Field(
        ...,
        example="cash",
        description="The type of payment for the receipt, can be either 'cash' or 'card'."
    )
    amount: float = Field(
        ...,
        example=150.75,
        description="The total amount paid for the receipt."
    )


class ReceiptRequestSchema(BaseModel):
    products: List[ReceiptItemSchema] = Field(
        ...,
        example=[
            {
                "title": "Laptop",
                "price": 899.99,
                "quantity": 1
            },
            {
                "title": "Phone Case",
                "price": 19.99,
                "quantity": 2
            }
        ],
        description="A list of products included in the receipt."
    )
    payment: ReceiptPaymentSchema = Field(
        ...,
        example={
            "type": "cash",
            "amount": 150.75
        },
        description="Payment information for the receipt, including type and amount."
    )

    class Config:
        orm_mode = True
