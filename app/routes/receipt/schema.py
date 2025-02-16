# coding=utf-8

from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel, Field


class ReceiptProductRequestSchema(BaseModel):
    title: str = Field(
        ...,
        example="Product Name",
        description="The name of the product/item included in the receipt."
    )
    price: Decimal = Field(
        ...,
        example=99.99,
        description="The price per unit of the product/item."
    )
    quantity: int = Field(
        ...,
        example=2.5,
        description="The quantity or weight of the product/item purchased."
    )

    class Config:
        extra = "forbid"


class ReceiptProductResponseSchema(ReceiptProductRequestSchema):
    total: Decimal = Field(
        ...,
        description="The total price for a single product, calculated by multiplying the quantity by price per unit."
    )

    class Config:
        from_attributes = True


class ReceiptPaymentSchema(BaseModel):
    type: str = Field(
        ...,
        example="cash",
        description="The type of payment for the receipt, can be either 'cash' or 'card'."
    )
    amount: Decimal = Field(
        ...,
        example=150.75,
        description="The total amount paid for the receipt."
    )


class ReceiptRequestSchema(BaseModel):
    products: list[ReceiptProductRequestSchema] = Field(
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

    total: Decimal = Field(
        ...,
        example=12.45,
        description="The total amount of the receipt, which is the sum of all product totals."
    )
    rest: Decimal = Field(
        ...,
        example=12.78,
        description="The remaining balance to be refunded to the user after the payment."
    )
    created_at: datetime = Field(
        ...,
        example=datetime.utcnow(),
        description="The timestamp when the receipt was created, represented in ISO 8601 format."
    )
    products: list[ReceiptProductResponseSchema] = Field(
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
    payment: ReceiptPaymentSchema = Field(
        ...,
        example={
            "type": "cash",
            "amount": 150.75
        },
        description="Payment information for the receipt, including type and amount."
    )

    class Config:
        from_attributes = True


class ReceiptsRequestSchema(BaseModel):
    start_date: datetime | None = Field(
        None,
        description="Optional filter for the start date of receipts.",
        example="2023-01-01T00:00:00Z"
    )
    end_date: datetime | None = Field(
        None,
        description="Optional filter for the end date of receipts.",
        example="2023-12-31T23:59:59Z"
    )
    total: Decimal | None = Field(
        None,
        description="Optional filter to get receipts with a total greater than or equal to this value.",
        example=100.00
    )
    payment_type: str | None = Field(
        None,
        description="Optional filter to get receipts based on payment type. Values: 'cash' or 'card'.",
        example="cash"
    )
    page: int = Field(
        1,
        description="Page number for pagination. Default is 1.",
        example=1
    )
    on_page: int = Field(
        10,
        description="Number of records to display per page. Default is 10.",
        example=10
    )


class ReceiptsResponseSchema(BaseModel):
    total: int = Field(
        ...,
        description="The total number of receipts available after applying filters.",
        example=100
    )
    page: int = Field(
        ...,
        description="The current page number in the pagination.",
        example=1
    )
    on_page: int = Field(
        ...,
        description="The number of receipts per page.",
        example=10
    )
    next_page: int | None = Field(
        None,
        description="The next page number if there are more results. If there are no more results, this will be null.",
        example=2
    )
    results: list[ReceiptResponseSchema]

    class Config:
        from_attributes = True
