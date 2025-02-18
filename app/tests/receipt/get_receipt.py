# coding=utf-8

from ..base import *
from .cases import RECEIPT_CREATION_TEST_CASES


@pytest.mark.asyncio
async def test_get_receipt_by_id(client: AsyncClient, db_session: AsyncSession):
    """
    Tests retrieving receipts by ID.
    """

    # Set default value
    created_receipt_ids = []
    receipts = RECEIPT_CREATION_TEST_CASES

    #  Register and log in a user
    user_data = {
        "first_name": "Test",
        "last_name": "User",
        "login": generate_random_username(),
        "password": "TestPassword123!"
    }

    # Register a new user
    reg_response = await client.post("/users/register", json=user_data)
    assert reg_response.status_code == 200, f"User registration failed: {reg_response.json()}"

    # Log in to obtain JWT token
    login_response = await client.post("/users/login", json={
        "login": user_data["login"],
        "password": user_data["password"]
    })
    assert login_response.status_code == 200, f"User login failed: {login_response.json()}"

    # Get access token
    access_token = login_response.json().get("access_token")
    assert access_token, "JWT token was not retrieved!"

    # Added access token to headers
    auth_headers = {"Authorization": f"Bearer {access_token}"}

    # Create multiple receipts and store their IDs
    receipt_data_list = [receipt for receipt in receipts if receipt["expected_status"] == 200]

    for receipt_data in receipt_data_list:
        response = await client.post(
            "/receipts/",
            json=receipt_data,
            headers=auth_headers
        )
        assert response.status_code == 200, f"Receipt creation failed: {response.json()}"

        receipt_id = response.json().get("id")
        assert receipt_id, "Receipt ID not found in response!"
        created_receipt_ids.append(receipt_id)

    # Retrieve receipts by valid IDs
    for receipt_id in created_receipt_ids:
        response = await client.get(f"/receipts/{receipt_id}", headers=auth_headers)
        assert response.status_code == 200, f"Failed to retrieve receipt {receipt_id}: {response.json()}"

        json_response = response.json()
        assert json_response["id"] == receipt_id, "Returned receipt ID does not match the requested ID!"

    # Step 4: Attempt retrieval of a non-existent receipt
    fake_receipt_id = max(created_receipt_ids) + 1000  # Assuming this ID does not exist
    response = await client.get(f"/receipts/{fake_receipt_id}", headers=auth_headers)
    assert response.status_code == 404, f"Expected 404 for non-existent receipt, got {response.status_code} instead!"
