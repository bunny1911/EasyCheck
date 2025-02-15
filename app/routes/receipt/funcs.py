# coding=utf-8

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import app.funcs.receipt.funcs as funcs
from app.funcs.user.funcs import get_user_id
from app.db import get_session

from .schema import ReceiptResponseSchema, ReceiptRequestSchema


receipt_router = APIRouter(
    prefix="/receipts",
    tags=["receipts"],
)


@receipt_router.post(
    "/",
    response_model=ReceiptResponseSchema
)
async def create_receipt(
    receipt_data: ReceiptRequestSchema,
    db_session: AsyncSession = Depends(get_session),
    user_id: int = Depends(get_user_id),

) -> dict:

    return await funcs.create_receipt(
        user_id=user_id,
        db_session=db_session,
        receipt_data=receipt_data,
    )


@receipt_router.get(
    "/{receipt_id}",
    response_model=ReceiptResponseSchema
)
async def get_receipt_by_id(
    receipt_id: int,
    db_session: AsyncSession = Depends(get_session),
) -> dict:

    return await funcs.get_receipt_by_id(
        db_session=db_session,
        receipt_id=receipt_id
    )
