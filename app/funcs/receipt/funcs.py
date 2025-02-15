from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from app.models import Receipt, ReceiptItem, User


async def create_receipt(
        db_session: AsyncSession,
        user_id: int,
        request_data: CreateReceiptRequestSchema
) -> ReceiptResponseSchema:
    """
    Function to create a receipt and calculate total values.

    Args:
        db_session (AsyncSession): Database session for interacting with the database.
        user_id (int): The user ID who is creating the receipt.
        request_data (CreateReceiptRequestSchema): Data for creating a receipt.

    Returns:
        ReceiptResponseSchema: The response schema containing the receipt data.
    """
    # Step 1: Calculate the total and total for each item
    total = 0
    items = []
    for product in request_data.products:
        item_total = product.price * product.quantity
        items.append(ReceiptItem(
            product_name=product.name,
            price=product.price,
            quantity=product.quantity,
            total=item_total
        ))
        total += item_total

    # Step 2: Calculate the rest
    payment_type = request_data.payment.type
    payment_amount = request_data.payment.amount
    rest = payment_amount - total

    if rest < 0:
        raise HTTPException(
            status_code=400,
            detail="Payment amount is less than the total"
        )

    # Step 3: Create a new receipt and add it to the database
    receipt = Receipt(
        user_id=user_id,
        total=total,
        payment_type=payment_type,
        payment_amount=payment_amount,
        rest=rest,
        items=items
    )

    db_session.add(receipt)
    await db_session.commit()
    await db_session.refresh(receipt)

    # Step 4: Return the response schema
    return
