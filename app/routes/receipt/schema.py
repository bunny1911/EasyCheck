# coding=utf-8
from typing import Literal
from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel, Field


class ReceiptProductRequestSchema(BaseModel):
    title: str = Field(
        ...,
        examples=["Product Name"],
        description="The name of the product/item included in the receipt."
    )
    price: Decimal = Field(
        ...,
        examples=[99.99],
        description="The price per unit of the product/item.",
        ge=0.1,
    )
    quantity: int = Field(
        ...,
        examples=[2.5],
        description="The quantity or weight of the product/item purchased.",
        ge=1,
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
    type: Literal["cash", "card"] = Field(
        ...,
        examples=["cash"],
        description="The type of payment for the receipt, can be either 'cash' or 'card'."
    )
    amount: Decimal = Field(
        ...,
        examples=[150.75],
        description="The total amount paid for the receipt."
    )


class ReceiptRequestSchema(BaseModel):
    products: list[ReceiptProductRequestSchema] = Field(
        ...,
        examples=[
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
        examples=[{
            "type": "cash",
            "amount": 150.75
        }],
        description="Payment information for the receipt, including type and amount."
    )


class ReceiptResponseSchema(BaseModel):
    id: int = Field(
        ...,
        examples=[12345],
        description="The unique identifier for the receipt."
    )

    total: Decimal = Field(
        ...,
        examples=[12.45],
        description="The total amount of the receipt, which is the sum of all product totals."
    )
    rest: Decimal = Field(
        ...,
        examples=[12.78],
        description="The remaining balance to be refunded to the user after the payment."
    )
    created_at: datetime = Field(
        ...,
        examples=[datetime.now()],
        description="The timestamp when the receipt was created, represented in ISO 8601 format."
    )
    products: list[ReceiptProductResponseSchema] = Field(
        ...,
        examples=[
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
        examples=[{
            "type": "cash",
            "amount": 150.75
        }],
        description="Payment information for the receipt, including type and amount."
    )

    class Config:
        from_attributes = True


class ReceiptsRequestSchema(BaseModel):
    start_date: datetime | None = Field(
        None,
        description="Optional filter for the start date of receipts.",
        examples=["2023-01-01T00:00:00Z"]
    )
    end_date: datetime | None = Field(
        None,
        description="Optional filter for the end date of receipts.",
        examples=["2023-12-31T23:59:59Z"]
    )
    total: Decimal | None = Field(
        None,
        description="Optional filter to get receipts with a total greater than or equal to this value.",
        examples=[100.00]
    )
    payment_type: Literal["cash", "card"] | None = Field(
        None,
        description="Optional filter to get receipts based on payment type.",
        examples=["cash"]
    )
    page: int = Field(
        0,
        description="Page number for pagination. Default is 0.",
        examples=[1]
    )
    on_page: int = Field(
        10,
        description="Number of records to display per page. Default is 10.",
        examples=[10]
    )


class ReceiptsResponseSchema(BaseModel):
    total: int = Field(
        ...,
        description="The total number of receipts available after applying filters.",
        examples=[100]
    )
    page: int = Field(
        ...,
        description="The current page number in the pagination.",
        examples=[1]
    )
    on_page: int = Field(
        ...,
        description="The number of receipts per page.",
        examples=[10]
    )
    next_page: int | None = Field(
        None,
        description="The next page number if there are more results. If there are no more results, this will be null.",
        examples=[2]
    )
    results: list[ReceiptResponseSchema]

    class Config:
        from_attributes = True


class ReceiptTextRequestSchema(BaseModel):
    width: int = Field(
        32,
        description="The maximum width (character length) of each line in the receipt text.",
        examples=[40, 80],
        ge=10,
        le=100
    )


class ReceiptTextResponseSchema(BaseModel):
    receipt_text: str = Field(
        ...,
        description="The receipt in a plain text format.",
        examples=[
            "             ФОП Micha Ber\n"
            "================================\n"
            "1 x 899.99                      \n"
            "Laptop                    899.99\n"
            "--------------------------------\n"
            "2 x 19.99                       \n"
            "Phone Case                 39.98"
            "\n--------------------------------\n"
            "1 x 899.99                      \n"
            "Laptop 1                  899.99\n"
            "--------------------------------\n"
            "2 x 19.99                       \n"
            "Phone Case 2               39.98\n"
            "================================\n"
            "СУМА                    1 879.94\n"
            "cash                    1 879.94\n"
            "Решта                     121.03\n"
            "================================\n"
            "        16.02.2025 18:18        \n"
            "      Дякуємо за покупку!"
        ]
    )
