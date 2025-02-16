
class ValidationValue:
    # Login Validation Rules
    login_regex = r"^[a-zA-Z0-9_]{5,32}$"
    login_min_length = 5
    login_max_length = 32

    # Password Validation Rules
    password_regex = r"^[A-Za-z\d@$!%*?&]{8,}$"
    password_min_length = 8
    password_max_length = 32


