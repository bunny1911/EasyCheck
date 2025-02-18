# coding=utf-8

from sqlalchemy.future import select
from app.models import User

from .cases import USER_REGISTER_TEST_CASE
from ..base import *


@pytest.mark.asyncio
@pytest.mark.parametrize("user_data, expected_status", USER_REGISTER_TEST_CASE)
async def test_create_user(
        client: AsyncClient,
        user_data: dict,
        expected_status: int,
        db_session: AsyncSession
):
    """
    Tests user registration and verifies database insertion using SQLAlchemy ORM.
    """

    # Defined response
    response = await client.post("/users/register", json=user_data)

    assert response.status_code == expected_status

    # Verify user exists in the database when status is 200
    if expected_status == 200:
        # Use SQLAlchemy ORM to query the database
        result = await db_session.execute(
            select(
                User
            ).where(
                User.login == user_data["login"]
            )
        )
        user = result.scalars().first()

        # Ensure user is found
        assert user is not None, "User was not inserted into the database!"

        # Check if the user matches the provided data
        assert user.first_name == user_data["first_name"], f"Expected {user_data['first_name']}, got {user.first_name}"
        assert user.last_name == user_data["last_name"], f"Expected {user_data['last_name']}, got {user.last_name}"
        assert user.login == user_data["login"], f"Expected {user_data['login']}, got {user.login}"
