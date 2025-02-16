# coding=utf-8

from typing import Literal
from datetime import datetime
from fastapi import HTTPException

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, Query
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
    receipt: Receipt | None = await db_session.scalar(
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
    page: int | None = 0,
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
    query: Query = select(
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
        query = query.filter(Receipt.payment_type == payment_type)

    # Defined total count of receipts
    total_receipts_result = await db_session.execute(
        select(
            func.count()
        ).select_from(
            query.subquery()
        )
    )
    total_receipts = total_receipts_result.scalar_one() or 0

    # Apply pagination
    query = query.limit(on_page).offset(page * on_page)

    # Defined receipts with pagination and filters
    results = await db_session.execute(query)
    receipts: list[Receipt] = results.scalars().unique().all()

    # Defined next page
    next_page = (page + 1 if on_page * (page + 1) < total_receipts else None)

    return {
        "total": total_receipts,
        "page": page,
        "on_page": on_page,
        "next_page": next_page,
        "results": receipts
    }


async def get_receipt_text(
    db_session: AsyncSession,
    receipt_id: int,
    width: int,
) -> dict:
    """"
    Retrieves the formatted text representation of a receipt.

    Args:
        db_session (AsyncSession): Database session for querying the receipt.
        receipt_id (int): The unique identifier of the receipt.
        width (int): The maximum number of characters per line in the receipt text.

    Raises:
        HTTPException: If no receipt is found with the given ID, raises a 404 error.

    Returns:
        dict: A dictionary containing the formatted receipt text.
    """

    # Get receipt from DB
    receipt: Receipt | None = await db_session.scalar(
        select(
            Receipt
        ).options(
            joinedload(
                Receipt.products
            ),
            joinedload(
                Receipt.user
            )
        ).where(
            Receipt.id == receipt_id,
        )
    )

    if not receipt:
        # Not found
        raise HTTPException(
            status_code=404,
            detail=f"Receipt with ID {receipt_id} not found"
        )

    # Defined receipt text
    receipt_text = get_total_text(
        receipt=receipt,
        width=width,
    )

    return receipt_text


def format_number(number: int | float) -> str:
    """
    Formats given number to string with spaces as thousands separator,
    and two decimal places.
    """

    return f"{number:,.2f}".replace(",", " ")


def split_words(words: list[str], max_width: int, hyphen: bool = True) -> list[str]:
    """
    For each word, split it into parts with maximum width.
    If word is shorter than max_width, return it as is.
    """

    new_words: list[str] = []

    for word in words:
        if len(word) <= max_width:
            # Word is short enough
            new_words.append(word)

        else:
            # Need to break it
            while len(word) > max_width:
                if hyphen:
                    # Break word into parts with hyphen
                    new_words.append(word[:max_width - 1] + "-")  # -1 for hyphen
                    word = word[max_width - 1:]

                else:
                    # Break word into parts without hyphen
                    new_words.append(word[:max_width])
                    word = word[max_width:]

            # Add remaining part
            new_words.append(word)

        if max_width == 1:
            # Add empty string to separate words
            new_words.append("")

    return new_words


def format_lines(
        width: int,
        min_spaces: int,
        left: str | None = None,
        right: str | None = None,
        left_hyphen: bool = True,
        right_hyphen: bool = True,
        priority: Literal["left", "right"] | None = None,
) -> str:
    """
    Format lines
    """

    # Validate
    assert left or right, "At least 'left' or 'right' parameter must be provided"
    assert width >= 1, "Width must be greater or equal to 1"
    assert min_spaces >= 0, "Minimum spaces must be greater than or equal to 0"
    assert width - min_spaces > 0, "Width must be greater than minimum spaces"

    # Split strings (or leave empty if None)
    left = left.split() if left else []
    right = right.split() if right else []

    # Break words if they are too long
    left = split_words(left, width - min_spaces, hyphen=left_hyphen)
    right = split_words(right, width - min_spaces, hyphen=right_hyphen)

    # We need to form center line (where both left and right are merged)
    if priority == "left" and len(" ".join(left)) < width - min_spaces:
        # Fit all left words + part of right words
        text = " ".join(left) + " " * min_spaces
        words = ""
        left = []  # All left words are used

        while right:
            if len(text) + len(words) + len(right[0]) + 1 > width:  # +1 for space between words
                # Too long
                break

            else:
                # Can fit => add word
                words = words + " " + right.pop(0)

        # Add spaces for fitter words
        words = " " * (width - len(text) - len(words)) + words

        # Add them to text
        text = text + words

    elif priority == "right" and len(" ".join(right)) < width - min_spaces:
        # Fit all right words + part of left words
        text = " " * min_spaces + " ".join(right)
        words = ""
        right = []  # All right words are used

        while left:
            if len(text) + len(words) + len(left[-1]) + 1 > width:  # +1 for space between words
                # Too long
                break

            else:
                # Can fit => add word
                words = left.pop(-1) + " " + words

        # Add spaces for fitter words
        words += " " * (width - len(text) - len(words))

        # Add them to text
        text = words + text

    else:
        # Try to fit middle line equally
        text = " " * min_spaces
        left_words = ""
        right_words = ""

        while left or right:
            # Try to add words from both sides while they exist

            if left:
                # Check for left word
                if len(text + left_words + right_words) + len(left[-1]) + 1 > width:
                    # Too long => fill with spaces & break
                    left_words = left_words + " " * (width - len(text + left_words + right_words))
                    break

                else:
                    # Can fit => add word
                    left_words = left.pop(-1) + " " + left_words

            if right:
                # Check for right word
                if len(text + left_words + right_words) + len(right[0]) + 1 > width:
                    # Too long => fill with spaces & break
                    right_words = " " * (width - len(text + left_words + right_words)) + right_words
                    break

                else:
                    # Can fit => add word
                    right_words = right_words + " " + right.pop(0)

        # Add them to text
        used_length = len(left_words + right_words)
        text = f"{left_words}{text: ^{width - used_length}}{right_words}"

    if left:
        # Left words left => fill lines with them
        lines = []
        line = left.pop(0)

        for word in left:
            if len(line) + len(word) + min_spaces + 1 > width:  # +1 for space
                # Too long => fill with spaces & break
                lines.append(f"{line: <{width}}")
                line = word

            else:
                line = line + " " + word

        # Add last line
        lines.append(f"{line: <{width}}")

        # Add them to text
        text = "\n".join(lines) + "\n" + text

    if right:
        # Right words left => fill lines with them
        lines = []
        line = right.pop(-1)

        for word in right:
            if len(line) + len(word) + min_spaces + 1 > width:  # +1 for space
                # Too long => fill with spaces & break
                lines.append(f"{line: >{width}}")
                line = word

            else:
                line = word + " " + line

        # Add last line
        lines.append(f"{line: >{width}}")

        # Add them to text
        text = text + "\n" + "\n".join(lines)

    return text


def format_center_lines(
        width: int,
        min_spaces: int,
        text: str | None = None,
        hyphen: bool = True,
) -> str:
    """
    Format center lines
    """

    # Validate
    assert width >= 1, "Width must be greater or equal to 1"
    assert min_spaces >= 0, "Minimum spaces must be greater than or equal to 0"
    assert width - min_spaces * 2 > 0, "Width must be greater than twice minimum spaces"

    # Split text into words
    words = text.split()

    # Break words if they are too long
    words = split_words(words, width - min_spaces * 2, hyphen=hyphen)

    # Form lines
    lines = []
    line = words.pop(0)

    for word in words:
        if len(line) + len(word) + min_spaces * 2 + 1 > width:  # +1 for space
            # Too long => fill with spaces & break
            lines.append(f"{line: ^{width}}")
            line = word

        else:
            line += " " + word

    # Add last line
    lines.append(f"{line: ^{width}}")

    return "\n".join(lines)


def get_total_text(receipt: Receipt, width: int = 32, min_spaces: int = 5) -> str:
    """
    Get formatted string of receipt.
    """

    # Prepare separators
    main_separator = "=" * width
    item_separator = "-" * width

    # Defined fool user-name
    user_name = f"ФОП  {receipt.user.first_name}  {receipt.user.last_name}"

    # Add header as first line
    lines: list[str] = [
        format_center_lines(
            width=width,
            min_spaces=min_spaces,
            text=user_name,
        ),
        main_separator,
    ]

    # Form lines for each item

    for index, product in enumerate(receipt.products):
        # Add count & price
        lines.append(
            format_lines(
                width=width,
                min_spaces=min_spaces,
                left=f"{product.quantity} x {format_number(product.price)}",
                left_hyphen=False,  # Break words without hyphen (because it's a numbers)
            ),
        )

        # Add title & total price
        lines.append(
            format_lines(
                width=width,
                min_spaces=min_spaces,
                left=product.title,
                right=format_number(product.total),
                right_hyphen=False,  # Break words without hyphen (because it's a numbers)
                priority="right",  # Priority to fit price
            ),
        )

        if index == len(receipt.products) - 1:
            # Is last => add main separator
            lines.append(main_separator)

        else:
            # Add item separator
            lines.append(item_separator)

    # Add sum
    lines.append(
        format_lines(
            width=width,
            min_spaces=min_spaces,
            left="СУМА",
            right=format_number(receipt.total),
            right_hyphen=False,  # Break words without hyphen (because it's a numbers)
            priority="left",  # Priority to fit "СУМА"
        ),
    )

    # Add payment
    lines.append(
        format_lines(
            width=width,
            min_spaces=min_spaces,
            left=receipt.payment_type,
            right=format_number(receipt.total),
            right_hyphen=False,  # Break words without hyphen (because it's a numbers)
            priority="left",  # Priority to fit payment type
        ),
    )

    # Add change
    lines.append(
        format_lines(
            width=width,
            min_spaces=min_spaces,
            left="Решта",
            right=format_number(receipt.rest),
            right_hyphen=False,  # Break words without hyphen (because it's a numbers)
            priority="left",  # Priority to fit "Решта"
        ),
    )

    # Add main separator
    lines.append(main_separator)

    # Add footer date & time
    lines.append(
        format_center_lines(
            width=width,
            min_spaces=min_spaces,
            text=receipt.created_at.strftime("%d.%m.%Y %H:%M"),
            hyphen=False,  # Break words without hyphen (because it's a date & time)
        ),
    )

    # Add footer message
    lines.append(
        format_center_lines(
            width=width,
            min_spaces=min_spaces,
            text="Дякуємо за покупку!",
            hyphen=False,  # Break words without hyphen (because it's a message)
        ),
    )

    # Create all text
    all_text = "\n".join(lines)

    return all_text
