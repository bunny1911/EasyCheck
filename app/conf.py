# coding=utf-8

import os
from dotenv import load_dotenv

# Loading all values from '.env' file
load_dotenv()

# Defined DB URL
DATABASE_URL = os.getenv("DATABASE_URL")
