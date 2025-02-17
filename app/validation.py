
class ValidationValue:
    # User nane validation rules
    user_regex = r"^[\p{L}']+$"
    user_min_length = 3

    # Login validation rules
    login_regex = r"^[a-zA-Z0-9_]{5,32}$"
    login_min_length = 5
    login_max_length = 32

    # Password validation rules
    password_regex = r"^[A-Za-z\d@$!%*?&]{8,}$"
    password_min_length = 8
    password_max_length = 32


