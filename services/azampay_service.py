import requests
import logging
from config import Config

# Configure logging
logging.basicConfig(filename=Config.LOG_FILE, level=logging.INFO, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

class AzamPayService:
    def __init__(self):
        self.token = None
        self.expire = None  # Optional: store expiration time if needed
    
    def get_token(self):
        """Get authentication token from AzamPay"""
        payload = {
            "appName": Config.AZAMPAY_APP_NAME,
            "clientId": Config.AZAMPAY_CLIENT_ID,
            "clientSecret": Config.AZAMPAY_CLIENT_SECRET
        }
        
        try:
            response = requests.post(Config.AZAMPAY_AUTH_URL, json=payload) 
            response.raise_for_status()  
            data = response.json()
            logging.info("Token response data: %s", data)
            
            # Extract the token from the "data" field using the key "accessToken"
            token_data = data.get("data", {})
            self.token = token_data.get("accessToken")
            self.expire = token_data.get("expire")  # Optional: use this for token caching logic
            
            if self.token:
                logging.info("Successfully obtained AzamPay token. Expires at: %s", self.expire)
            else:
                logging.error("Token not found in response: %s", data)
            
            return self.token
        except requests.exceptions.RequestException as e:
            logging.error("Failed to obtain AzamPay token: %s", e)
            return None

    def mno_checkout(self, account_number, amount, external_id, provider):
        """Initiate MNO payment"""
        if not self.token:
            self.get_token()
        if not self.token:
            logging.error("Token retrieval failed. Cannot proceed with MNO checkout.")
            return None

        headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
        payload = {
            "accountNumber": account_number,
            "amount": amount,
            "currency": "TZS",
            "externalId": external_id,
            "provider": provider
        }

        try:
            response = requests.post(Config.AZAMPAY_MNO_CHECKOUT_URL, json=payload, headers=headers)
            response.raise_for_status()
            logging.info("MNO Checkout request successful.")
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to initiate MNO Checkout: {e}")
            return None



# """
# AzamPay Service Module

# This module provides functions to interact with the AzamPay API, including obtaining an authentication token and 
# initiating a payment transaction.
# """

# import time # For timestamping the token expiry
# import requests
# import logging
# from config import (
#     AZAMPAY_PAYMENT_URL, AZAMPAY_AUTH_URL, AZAMPAY_APP_NAME, AZAMPAY_API_KEY, AZAMPAY_CLIENT_ID, AZAMPAY_CLIENT_SECRET, CALLBACK_URL
# )

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Simple in-memory cache for the token
# _cached_token = None
# _token_expiry = 0  # Unix timestamp when token expires

# def get_azam_token():
#     """
#     Obtain and cache an access token from AzamPay.
#     If a valid token is already cached, return it instead of making a new request.
#     """
#     global _cached_token, _token_expiry

#     # If we have a token and it's not expired, return it.
#     if _cached_token and time.time() < _token_expiry:
#         logger.info("Using cached AzamPay token.")
#         return _cached_token
    
#     """
#     Obtain an access token from AzamPay using client credentials.

#     Returns:
#         token (str): The access token if the request is successful.
#         None: If there is an error during token retrieval.
#     """
#     payload = {
#         "appName": AZAMPAY_APP_NAME,
#         "clientId": AZAMPAY_CLIENT_ID,
#         "clientSecret": AZAMPAY_CLIENT_SECRET
#     }
#     headers = { "Content-Type": "application/json"}

#     try:
#         response = requests.post(AZAMPAY_AUTH_URL, json=payload, headers=headers)
#         response.raise_for_status()
#         data = response.json()
#         token = data.get("accessToken")
#         logger.info("Successfully obtained AzamPay token.")
#         return token
#     except requests.RequestException as e:
#         logger.error("Failed to obtain AzamPay token: %s", e)
#         return None
    
# def mno_checkout(account_number, amount, currency, external_id, provider, additional_properties=None):
#     """
#     Initiate an MNO checkout payment via AzamPay.
    
#     This function makes a POST request to the AzamPay sandbox MNO checkout endpoint,
#     which processes payments through a Mobile Network Operator (MNO).
    
#     Args:
#         account_number (str): The account number/MSISDN of the consumer.
#         amount (str): The amount to be charged.
#         currency (str): The transaction currency (e.g., "TZS").
#         external_id (str): An identifier provided by your application (max 128 characters).
#         provider (str): The mobile network provider. Allowed values are "Airtel", "Tigo",
#                         "Halopesa", "Azampesa", "Mpesa".
#         additional_properties (dict, optional): Any additional JSON data to include.
    
#     Returns:
#         dict: The JSON response from AzamPay if successful.
#         None: If the payment initiation fails.
#     """
#     token = get_azam_token()
#     if not token:
#         logger.error("Token retrieval failed. Cannot proceed with MNO checkout.")
#         return None

#     payload = {
#         "accountNumber": account_number,
#         "amount": amount,
#         "currency": currency,
#         "externalId": external_id,
#         "provider": provider,
#         "additionalProperties": additional_properties or {}  # Use an empty dict if not provided
#     }

#     headers = {
#         "Authorization": f"Bearer {token}",
#         "Content-Type": "application/json",
#         "Accept": "application/json"
#     }

#     mno_checkout_url = "https://sandbox.azampay.co.tz/azampay/mno/checkout"
#     logger.info("Initiating MNO checkout at: %s", mno_checkout_url)
    
#     try:
#         response = requests.post(mno_checkout_url, json=payload, headers=headers)
#         response.raise_for_status()
#         logger.info("MNO checkout successful. Response: %s", response.json())
#         return response.json()
#     except requests.RequestException as e:
#         logger.error("MNO checkout failed: %s", e)
#         return None    
