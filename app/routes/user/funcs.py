# coding=utf-8

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import app.funcs.user.funcs as funcs
from app.db import get_session

from .schema import *


user_router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@user_router.post(
    "/register",
    response_model=UserResponseRegisterSchema,
)
async def create_user(
    user: UserRequestRegisterSchema,
    db_session: AsyncSession = Depends(get_session)
) -> dict:
    """
    Endpoint for user registration.
    It accepts user data, creates a new user in the database, and returns the created user object.
    """

    return await funcs.create_user(
        db_session=db_session,
        first_name=user.first_name,
        last_name=user.last_name,
        login=user.login,
        password=user.password
    )


@user_router.post(
    "/login",
    response_model=UserResponseLoginSchema
)
async def login_user(
    user: UserRequestLoginSchema,
    db_session: AsyncSession = Depends(get_session)
) -> dict:
    """
    Endpoint for user registration.
    It accepts user data, creates a new user in the database, and returns the created user object.
    """

    return await funcs.login_user(
        db_session=db_session,
        login=user.login,
        password=user.password
    )
