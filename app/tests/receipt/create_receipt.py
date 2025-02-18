# coding=utf-8

import random
import string

from app.models import Receipt

from ..base import *
from .cases import RECEIPT_CREATION_TEST_CASES


def generate_random_username(prefix="test_user_", length=8):
    """
    Generates a random username that meets the required regex pattern.
    """

    random_part = ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    return f"{prefix}{random_part}"


@pytest.mark.asyncio
@pytest.mark.parametrize("receipt_data", RECEIPT_CREATION_TEST_CASES)
async def test_create_receipt(client: AsyncClient, db_session: AsyncSession, receipt_data: dict):
    """
    Tests receipt creation with authorization and database validation.
    Each test independently registers and logs in a user to obtain a JWT token.
    """

    # Generate a valid random username
    user_data = {
        "first_name": "Test",
        "last_name": "User",
        "login": generate_random_username(),
        "password": "TestPassword123!"
    }

    # Register a new user
    reg_response = await client.post("/users/register", json=user_data)
    assert reg_response.status_code == 200, f"User registration failed: {reg_response.json()}"

    # Login to obtain a JWT token
    login_response = await client.post("/users/login", json={
        "login": user_data["login"],
        "password": user_data["password"]
    })
    assert login_response.status_code == 200, f"User login failed: {login_response.json()}"

    # Extract JWT token
    access_token = login_response.json().get("access_token")
    assert access_token, "JWT token was not retrieved!"

    auth_headers = {"Authorization": f"Bearer {access_token}"}

    # Send request to create a receipt
    response = await client.post(
        "/receipts/",
        json={
            "products": receipt_data["products"],
            "payment": receipt_data["payment"]
        },
        headers=auth_headers  # Add authentication header
    )

    assert response.status_code == receipt_data["expected_status"], (
        f"Expected {receipt_data['expected_status']} for receipt creation, "
        f"but got {response.status_code}. Response: {response.json()}"
    )

    # If the receipt is expected to be stored in the database, verify its presence
    if receipt_data["check_db"]:
        json_response = response.json()
        receipt_id = json_response.get("id")

        assert receipt_id is not None, "Missing receipt ID in the response!"

        # Retrieve the receipt from the database
        db_receipt: Receipt | None = await db_session.get(Receipt, receipt_id)
        assert db_receipt is not None, f"Receipt with ID {receipt_id} was not found in the database!"
