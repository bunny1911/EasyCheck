# coding=utf-8

import os
from dotenv import load_dotenv


# Loading all values from '.env' file
load_dotenv()

# Defined secret key
SECRET_KEY = os.getenv("SECRET_KEY")

# Defined encryption algorithm
ALGORITHM = os.getenv("ALGORITHM")


# Defined DB URL
DATABASE_URL = (
    f"postgresql+asyncpg://"
    f"{os.getenv('DATABASE_USERNAME')}:"
    f"{os.getenv('DATABASE_PASSWORD')}@"
    f"{os.getenv('DATABASE_HOST')}:"
    f"{os.getenv('DATABASE_PORT')}/"
    f"{os.getenv('DATABASE_NAME')}"
)


TEST_DATABASE_URL = (
    f"postgresql+asyncpg://"
    f"{os.getenv('TEST_DATABASE_USERNAME')}:"
    f"{os.getenv('TEST_DATABASE_PASSWORD')}@"
    f"{os.getenv('TEST_DATABASE_HOST')}:"
    f"{os.getenv('TEST_DATABASE_PORT')}/"
    f"{os.getenv('TEST_DATABASE_NAME')}"
)
