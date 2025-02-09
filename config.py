import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables from the .env file

class Config:
    # Log file for storing application logs
    LOG_FILE = os.getenv("LOG_FILE")

    # AzamPay API endpoints and credentials
    AZAMPAY_AUTH_URL = os.getenv("AZAMPAY_AUTH_URL")
    AZAMPAY_MNO_CHECKOUT_URL = os.getenv("AZAMPAY_MNO_CHECKOUT_URL")
    AZAMPAY_APP_NAME = os.getenv("AZAMPAY_APP_NAME")
    AZAMPAY_CLIENT_ID = os.getenv("AZAMPAY_CLIENT_ID")
    AZAMPAY_CLIENT_SECRET = os.getenv("AZAMPAY_CLIENT_SECRET")

    # Callback URL for notifying integrated platform after payment processing
    CALLBACK_URL = os.getenv("CALLBACK_URL")
