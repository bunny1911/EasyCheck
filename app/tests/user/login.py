# coding=utf-8

from ..base import *
from .cases import USER_LOGIN_TEST_CASE


@pytest.mark.asyncio
@pytest.mark.parametrize("user_data", USER_LOGIN_TEST_CASE)
async def test_register_and_login(client: AsyncClient, user_data: dict):
    """
    Registers a user and immediately attempts to log in.
    Registration is always successful.
    Login may fail based on `expected_login_status`.
    """

    # Register the user (should always succeed)
    reg_response = await client.post("/users/register", json={
        "first_name": user_data["first_name"],
        "last_name": user_data["last_name"],
        "login": user_data["login"],
        "password": user_data["password"]
    })

    assert reg_response.status_code == 200, (
        f"User registration failed! Response: {reg_response.json()}"
    )

    # Attempt login with modified credentials
    login_response = await client.post("/users/login", json={
        "login": user_data["login_attempt"],
        "password": user_data["password_attempt"]
    })

    assert login_response.status_code == user_data["expected_login_status"], (
        f"Expected {user_data['expected_login_status']} for"
        f" login, but got {login_response.status_code}. Response: {login_response.json()}"
    )
