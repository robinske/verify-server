import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
SERVICE_SID = os.environ.get('VERIFY_SERVICE_SID')