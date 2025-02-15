from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class ReceiptProductSchema(BaseModel):
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
        alias="receipt.amount",
        example=150.75,
        description="The total amount paid for the receipt."
    )


class ReceiptRequestSchema(BaseModel):
    products: List[ReceiptProductSchema] = Field(
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


class ReceiptResponseSchema(BaseModel):
    id: int = Field(
        ...,
        example=12345,
        description="The unique identifier for the receipt."
    )

    total: float = Field(
        ...,
        example=12.45,
        description="The total amount of the receipt, which is the sum of all product totals."
    )
    rest: float = Field(
        ...,
        example=12.78,
        description="The remaining balance to be refunded to the user after the payment."
    )
    created_at: datetime = Field(
        ...,
        example=datetime.utcnow(),
        description="The timestamp when the receipt was created, represented in ISO 8601 format. This field is optional."
    )
    products: List[ReceiptProductSchema] = Field(
        ...,
        example=[
            {
                "title": "Laptop",
                "price": 899.99,
                "quantity": 1,
                "total": 899.99,
            },
            {
                "title": "Phone Case",
                "price": 19.99,
                "quantity": 2,
                "total": 39.98,
            }
        ],
        description="A list of products included in the receipt."
    )
    # payment: ReceiptPaymentSchema = Field(
    #     ...,
    #     example={
    #         "type": "cash",
    #         "amount": 150.75
    #     },
    #     description="Payment information for the receipt, including type and amount."
    # )

    class Config:
        orm_mode = True
