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
        
    def forward_callback(self, callback_data):
        """
        Forward the callback data received from AzamPay to the frontend platform application's callback endpoint.
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        try:
            response = requests.post(Config.CALLBACK_URL, json=callback_data, headers=headers, timeout=10)
            response.raise_for_status()
            logging.info("Callback forwarded to frontend platform successfully. Response: %s", response.json())
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error("Failed to forward callback to frontend platform: %s", e)
            return None

