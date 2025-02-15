# coding=utf-8

from datetime import datetime
from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.future import select

from app.routes.receipt.schema import ReceiptRequestSchema
from app.models import Receipt, ReceiptProduct


async def create_receipt(
        user_id: int,
        db_session: AsyncSession,
        receipt_data: ReceiptRequestSchema
) -> dict:
    """
    Function to create a receipt and calculate total values.

    Args:
        user_id (int): The user ID who is creating the receipt.
        db_session (AsyncSession): Database session for interacting with the database.
        receipt_data (ReceiptRequestSchema): Data for creating a receipt.

    Returns:
        dict: Created receipt with include information
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
        db_session=db_session,
        user_id=user_id
    )


async def get_receipt(
    receipt_id: int,
    user_id: int,
    db_session: AsyncSession
) -> dict:
    """
    Function to retrieve a receipt by its ID, including associated items and payment method.

    Args:
        receipt_id (int): The ID of the receipt to be retrieved.
        user_id (int): The user ID who want to get receipt.
        db_session (AsyncSession): The database session for interacting with the database.

    Raises:
        HTTPException: If no receipt is found with the given ID, raises a 404 error.

    Returns:
        dict: The receipt data including its ID, products, payment info, and other details.
    """

    # Get receipt from DB
    receipt = await db_session.scalar(
        select(
            Receipt
        ).options(
            joinedload(
                Receipt.products
            ),
        ).where(
            Receipt.id == receipt_id,
            Receipt.user_id == user_id,
        )
    )

    if not receipt:
        # Not found
        raise HTTPException(
            status_code=404,
            detail=f"Receipt with ID {receipt_id} not found"
        )

    return receipt


async def get_receipts(
    db_session: AsyncSession,
    user_id: int,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    total: float | None = None,
    payment_type: str | None = None,
    page: int | None = 1,
    on_page: int | None = 10
) -> dict:
    """
    Function to retrieve a list of receipts for a user, applying filters and pagination.
    We first fetch all receipts for the user, apply filters, and then calculate totals and pagination.

    Args:
        db_session (AsyncSession): The database session.
        user_id (int): The ID of the user whose receipts we are fetching.
        start_date (datetime | None): Filter receipts by start date.
        end_date (datetime | None): Filter receipts by end date.
        total (float | None): Filter receipts with a total greater than or equal to the given value.
        payment_type (str | None): Filter by payment type (cash or card).
        page (int): The page number for pagination.
        on_page (int): The number of records per page.

    Returns:
        dict: The filtered and paginated list of receipts with total calculations.
    """

    # Create a base query for receipts
    query = select(
        Receipt
    ).options(
        joinedload(
            Receipt.products
        )
    ).filter(
        Receipt.user_id == user_id
    )

    # Filters
    if start_date:
        # Filter by start data
        query = query.filter(Receipt.created_at >= start_date)

    if end_date:
        # Filter by end data
        query = query.filter(Receipt.created_at <= end_date)

    if total is not None:
        # Filter by total price of receipt
        query = query.filter(Receipt.total >= total)

    if payment_type:
        # # Filter by payment type
        query = query.join(Receipt.payment_method).filter(Receipt.payment_method.title == payment_type)

    # Apply pagination
    query = query.offset((page - 1) * on_page).limit(on_page)

    # Defined receipts with pagination and filters
    results = await db_session.execute(query)
    receipts = results.scalars().unique().all()

    # Defined total count of results
    total = len(receipts)

    # Defined next page
    next_page = page + 1 if len(receipts) == on_page else None

    return {
        "total": total,
        "page": page,
        "on_page": on_page,
        "next_page": next_page,
        "results": receipts
    }
