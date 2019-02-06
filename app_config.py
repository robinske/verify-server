import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

AUTHY_API_KEY = os.environ['AUTHY_API_KEY']