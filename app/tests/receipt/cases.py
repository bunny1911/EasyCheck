# coding=utf-8

RECEIPT_CREATION_TEST_CASES = [
    {
        "products": [
            {"title": "Laptop", "price": 899.99, "quantity": 1},
            {"title": "Phone Case", "price": 19.99, "quantity": 2},
        ],
        "payment": {"type": "cash", "amount": 939.97},
        "expected_status": 200,
        "check_db": True
    },
    {
        "products": [
            {"title": "Book", "price": 15.50, "quantity": 3},
        ],
        "payment": {"type": "card", "amount": 46.50},
        "expected_status": 200,
        "check_db": True
    },
    {
        "products": [],
        "payment": {"type": "cash", "amount": 0},
        "expected_status": 422,
        "check_db": False
    },
    {
        "products": [
            {"title": "Invalid Product", "price": -5.00, "quantity": 1},
        ],
        "payment": {"type": "cash", "amount": 5.00},
        "expected_status": 422,
        "check_db": False
    },
    {
        "products": [
            {"title": "Laptop", "price": 899.99, "quantity": 1}
        ],
        "payment": {"type": "crypto", "amount": 899.99},
        "expected_status": 422,
        "check_db": False
    }
]
