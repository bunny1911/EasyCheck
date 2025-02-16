# coding=utf-8

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import app.funcs.receipt.funcs as funcs
from app.funcs.user.funcs import get_user_id
from app.db import get_session

from .schema import *


receipt_router = APIRouter(
    prefix="/receipts",
    tags=["receipts"],
)


@receipt_router.post(
    "/",
    response_model=ReceiptResponseSchema,
)
async def create_receipt(
    receipt_data: ReceiptRequestSchema,
    db_session: AsyncSession = Depends(get_session),
    user_id: int = Depends(get_user_id),
) -> dict:
    """
    Endpoint for create a new receipt based on the provided data.
    """

    return await funcs.create_receipt(
        user_id=user_id,
        db_session=db_session,
        receipt_data=receipt_data,
    )


@receipt_router.get(
    "/{receipt_id}",
    response_model=ReceiptResponseSchema,
)
async def get_receipt_by_id(
    receipt_id: int,
    user_id: int = Depends(get_user_id),
    db_session: AsyncSession = Depends(get_session),
) -> dict:
    """
    Endpoint for retrieve a receipt by its unique ID, including associated products and payment details.
    """

    return await funcs.get_receipt(
        db_session=db_session,
        receipt_id=receipt_id,
        user_id=user_id,
    )


@receipt_router.get(
    "/",
    response_model=ReceiptsResponseSchema,
)
async def get_receipts(
    db_session: AsyncSession = Depends(get_session),
    user_id: int = Depends(get_user_id),
    filters_data: ReceiptsRequestSchema = Depends(),

) -> dict:
    """
    Endpoint for retrieve a list of receipts, including associated products and payment details.
    """

    return await funcs.get_receipts(
        user_id=user_id,
        db_session=db_session,
        start_date=filters_data.start_date,
        end_date=filters_data.end_date,
        total=filters_data.total,
        payment_type=filters_data.payment_type,
        page=filters_data.page,
        on_page=filters_data.on_page,
    )
