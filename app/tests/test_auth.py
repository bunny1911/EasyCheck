from .base import *


import pytest
from fastapi.testclient import TestClient

VALID_USER = {
    "first_name": "Test",
    "last_name": "User",
    "login": "testuser",
    "password": "securepassword"
}


@pytest.mark.parametrize(
    "first_name, last_name, expected_status",
    [
        ("John", "Doe", 200),  # Valid English names
        ("Jean-Luc", "Picard", 422),  # Hyphens are not allowed in the name
        ("12345", "Smith", 422),  # Numbers are not allowed in the name
        ("", "User", 422),  # Empty first name is not allowed
        ("Test", "", 422),  # Empty last name is not allowed
        ("Test ", "User", 422),  # Trailing spaces in the name are not allowed
        (" Test", "User", 422),  # Leading spaces in the name are not allowed
        ("Test Test", "User", 422),  # Spaces inside the name are not allowed
        ("John", "Doe123", 422),  # Numbers are not allowed in the last name
        ("😊", "User", 422),  # Emojis are not allowed in the name
    ]
)
def test_register_user_name(client: TestClient, first_name, last_name, expected_status):
    response = client.post(
        "/users/register",
        json={
            **VALID_USER,
            "first_name": first_name,
            "last_name": last_name
        }
    )
    assert response.status_code == expected_status

