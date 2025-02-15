# coding=utf-8

import os
from dotenv import load_dotenv


# Loading all values from '.env' file
load_dotenv()

# Defined DB URL
DATABASE_URL = os.getenv("DATABASE_URL")

# Defined secret key
SECRET_KEY = os.getenv("SECRET_KEY")

# Defined encryption algorithm
ALGORITHM = os.getenv("ALGORITHM")


