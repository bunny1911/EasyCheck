# coding=utf-8

USER_REGISTER_TEST_CASE = [
    # Valid Cases with different username, login & password combinations
    ({"first_name": "John", "last_name": "Doe", "login": "testuser1", "password": "securepassword"}, 200),
    ({"first_name": "Artur", "last_name": "Smith", "login": "alice99", "password": "mypassword123"}, 200),
    ({"first_name": "Maria", "last_name": "Lopez", "login": "maria_2025", "password": "StrongPass!2025"}, 200),
    ({"first_name": "User", "last_name": "Test", "login": "test_user", "password": "12345678"}, 200),  # Simple password
    ({"first_name": "Admin", "last_name": "Super", "login": "admin_user", "password": "Admin!1234"}, 200),

    # Not Valid Cases (missing fields)
    ({}, 422),
    ({"first_name": "John"}, 422),
    ({"last_name": "Doe"}, 422),
    ({"login": "testuser1"}, 422),
    ({"password": "secure_password"}, 422),
    ({"first_name": "John", "last_name": "Doe", "login": "testuser1"}, 422),
    ({"first_name": "John", "last_name": "Doe", "password": "securepassword"}, 422),

    # Invalid Login Cases
    ({"first_name": "John", "last_name": "Doe", "login": "", "password": "securepassword"}, 422),
    ({"first_name": "John", "last_name": "Doe", "login": "a", "password": "securepassword"}, 422),
    ({"first_name": "John", "last_name": "Doe", "login": "t" * 33, "password": "securepassword"}, 422),
    ({"first_name": "John", "last_name": "Doe", "login": "john@doe", "password": "securepassword"}, 422),
    ({"first_name": "John", "last_name": "Doe", "login": "john doe", "password": "securepassword"}, 422),
    ({"first_name": "John", "last_name": "Doe", "login": "test!", "password": "securepassword"}, 422),

    # Invalid Password Cases
    ({"first_name": "John", "last_name": "Doe", "login": "user123", "password": ""}, 422),
    ({"first_name": "John", "last_name": "Doe", "login": "user123", "password": "123"}, 422),
    ({"first_name": "John", "last_name": "Doe", "login": "user123", "password": "      "}, 422),
    ({"first_name": "John", "last_name": "Doe", "login": "user123", "password": "P@ss w0rd!"}, 422),

    # Existing login
    ({"first_name": "John", "last_name": "Doe", "login": "login1", "password": "securepassword"}, 200),
    ({"first_name": "John", "last_name": "Doe", "login": "login1", "password": "securepassword"}, 400)
]

USER_LOGIN_TEST_CASE = [
    # Valid users (should pass registration and login)
    {
        "first_name": "John", "last_name": "Doe", "login": "testuser1", "password": "Secure123!",
        "expected_login_status": 200, "login_attempt": "testuser1", "password_attempt": "Secure123!"
    },
    {
        "first_name": "Alice", "last_name": "Smith", "login": "alice99", "password": "Pa$$w0rd",
        "expected_login_status": 200, "login_attempt": "alice99", "password_attempt": "Pa$$w0rd"
    },
    {
        "first_name": "Robert", "last_name": "Brown", "login": "robert_b", "password": "Admin!2024",
        "expected_login_status": 200, "login_attempt": "robert_b", "password_attempt": "Admin!2024"
    },

    # Invalid logins (registration succeeds, login fails)
    {
        "first_name": "Invalid", "last_name": "User", "login": "invalid_user", "password": "ValidPass123!",
        "expected_login_status": 401, "login_attempt": "invalid_user", "password_attempt": "wrongpassword"
    },

    # Invalid passwords (registration succeeds, login fails)
    {
        "first_name": "Test", "last_name": "User", "login": "test_login", "password": "SecurePass!",
        "expected_login_status": 422, "login_attempt": "test_login", "password_attempt": "123"
    },
    {
        "first_name": "Short", "last_name": "Pwd", "login": "short_pwd", "password": "StrongPass!",
        "expected_login_status": 422, "login_attempt": "short_pwd", "password_attempt": "pass"
    },
]
