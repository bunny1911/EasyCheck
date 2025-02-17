# coding=utf-8

from .base import *


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


@pytest.mark.parametrize(
    "login, expected_status",
    [
        ("wheel_smet", 200),  # Valid login: lowercase letters, underscore
        ("user.name", 422),  # Valid login: dot is allowed
        ("user-name", 422),  # Hyphens are not allowed
        ("user name", 422),  # Spaces are not allowed
        ("user@name", 422),  # Special characters like '@' are not allowed
        ("", 422),  # Empty login is not allowed
        ("sh", 422),  # Too short login (assuming min_length > 2)
        ("a" * 51, 422),  # Too long login (assuming max_length = 50)
        ("😊username", 422),  # Emojis are not allowed
        ("user.name_123", 422),  # Combination of dot, underscore, and numbers
    ]
)
def test_register_user_login(client: TestClient, login, expected_status):
    """
    Tests the validation of login during user registration.
    """
    response = client.post(
        "/users/register",
        json={
            **VALID_USER,
            "login": login
        }
    )

    # Print response JSON if test fails
    assert response.status_code == expected_status, response.json()


@pytest.mark.parametrize(
    "password, expected_status",
    [
        ("StrongPass123!", 200),  # Valid password: contains letters, numbers, and special characters
        ("short", 422),  # Too short password (assuming min_length = 8)
        ("a" * 33, 422),  # Too long password (assuming max_length = 32
        ("spaced out", 422),  # Spaces are not allowed in the password
        ("P@ssword😊", 422),  # Emojis are not allowed in the password
        ("P@ ssword", 422),  # Spaces inside the password are not allowed
    ]
)
def test_register_user_password(client: TestClient, password, expected_status):
    """
    Tests the validation of password during user registration.
    """
    response = client.post(
        "/users/register",
        json={
            **VALID_USER,
            "password": password
        }
    )

    # Print response JSON if test fails
    assert response.status_code == expected_status, response.json()
