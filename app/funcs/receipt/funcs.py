
from app.routes.receipt.schema import ReceiptRequestSchema
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from fastapi import HTTPException
from sqlalchemy.future import select
from app.models import Receipt, ReceiptProduct


async def create_receipt(
        user_id: int,
        db_session: AsyncSession,
        receipt_data: ReceiptRequestSchema
) -> dict:
    """
    Function to create a receipt and calculate total values.

    Args:
        db_session (AsyncSession): Database session for interacting with the database.
        user_id (int): The user ID who is creating the receipt.
        receipt_data (ReceiptRequestSchema): Data for creating a receipt.

    Returns:
        ReceiptResponseSchema: The response schema containing the receipt data.
    """

    # Set default value
    total = 0
    items = []

    for product in receipt_data.products:
        # Defined total price for item
        item_total = product.price * product.quantity

        items.append(
            ReceiptProduct(
                title=product.title,
                price=product.price,
                quantity=product.quantity,
            ))

        # Defined total price for receipt
        total += item_total

    # Defined 'rest' value for receipt
    rest = receipt_data.payment.amount - total

    # Step 3: Create a new receipt and add it to the database
    receipt = Receipt(
        user_id=user_id,
        total=total,
        payment_type=receipt_data.payment.type,
        payment_amount=receipt_data.payment.amount,
        rest=rest,
        products=items
    )

    # Save all changes
    db_session.add(receipt)
    await db_session.commit()
    await db_session.refresh(receipt)

    return await get_receipt(
        receipt_id=receipt.id,
        db_session=db_session
    )


async def get_receipt(
    receipt_id: int,
    db_session: AsyncSession
) -> dict:
    """
    Function to retrieve a receipt by its ID, including associated items and payment method.

    Args:
        receipt_id (int): The ID of the receipt to be retrieved.
        db_session (AsyncSession): The database session for interacting with the database.

    Raises:
        HTTPException: If no receipt is found with the given ID, raises a 404 error.

    Returns:
        dict: The receipt data including its ID, products, payment info, and other details.
    """

    # Retrieve the receipt from the database with its related items and payment method
    receipt = await db_session.scalar(
        select(
            Receipt
        ).options(
            joinedload(
                Receipt.products
            ),
        ).where(Receipt.id == receipt_id)
    )

    if not receipt:
        # If no receipt found with the given ID, raise an error
        raise HTTPException(
            status_code=404,
            detail=f"Receipt with ID {receipt_id} not found"
        )

    # Return the receipt data in a structured format
    return receipt
