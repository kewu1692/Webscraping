import os
from dotenv import load_dotenv

load_dotenv()
user = os.getenv("user")
host = os.getenv("host")
password = os.getenv("password")

