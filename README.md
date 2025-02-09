# Python Payment Gateway with AzamPay Integration

This project implements a Python-based payment gateway using Flask that integrates with the AzamPay sandbox API. It supports:

- **Token Generation**: Obtaining an access token from AzamPay.
- **MNO Checkout**: Initiating mobile money payments via AzamPay's MNO Checkout endpoint.
- **Callback Handling**: Receiving transaction status notifications from AzamPay.

This backend is designed to work in tandem with a frontend app, where the application sends payment details to this Python service and receives transaction status updates via callbacks.

## Project Structure

```
/GATEWAY MONEY API
    ├── gateway.py               # Main Flask application with API endpoints.
    ├── config.py                # Configuration loader (handles environment variables).
    ├── services/
    │   ├── __init__.py          # Package initializer.
    │   └── azampay_service.py   # Contains functions for token generation, MNO checkout, etc.
    ├── logs/
    │   └── gateway.log          # Log file for application logging.
    ├── requirements.txt         # Python dependencies.
    └── README.md                # This documentation file.
```

## Features

- Token Generation: Retrieves an access token from AzamPay using your credentials.
- MNO Checkout: Receives payment details from a Laravel frontend and forwards them to AzamPay to process mobile money payments.
- Callback Endpoint: Provides an always-available endpoint (/api/v1/Checkout/Callback) to receive transaction completion notifications from AzamPay.
- Error Handling & Logging: Detailed logging of all operations to help with debugging and monitoring.

## Setup and Installation

### Prerequisites
- Python 3.7 or higher
- pip
- (Optional) virtualenv
- (Optional) ngrok for exposing your local server

### Steps
1. Clone the Repository
    ```sh
    git clone https://github.com/DulshanRerg/python-payment-gateway.git
    cd python-payment-gateway
    ```
2. Create and Activate a Virtual Environment
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3. Install Dependencies
    ```sh
    pip install -r requirements.txt
    ```
4. Configure Environment Variables
    The project uses a configuration file (config.py) to manage settings. Key variables include:
    ```
    AZAMPAY_APP_NAME: The name of your application.
    AZAMPAY_CLIENT_ID: Your AzamPay client ID.
    AZAMPAY_CLIENT_SECRET: Your AzamPay client secret.
    AUTH_URL: The AzamPay token generation endpoint.
    MNO_CHECKOUT_URL: The AzamPay MNO checkout endpoint.
    CALLBACK_URL: The URL that AzamPay will call to send payment status updates.
    ```
    Environment variables are loaded using python-dotenv from the .env file.

## Run the Application
    ```sh
    python gateway.py
    ```

    The application will run on http://0.0.0.0:5000.

### (Optional) Expose Locally with ngrok

If you need to test the callback endpoint externally (e.g., from AzamPay), run:
```sh
ngrok http 5000
```
Use the provided ngrok URL (e.g., https://<ngrok-id>.ngrok-free.app/api/v1/Checkout/Callback) as your callback URL in AzamPay's settings.

## Developer Information

- **Author**: Abdul Rajabu
- **Email**: dulshanrerg@duck.com
- **GitHub**: [DulshanRerg](https://github.com/DulshanRerg)

## License
This project is provided as-is for demonstration purposes. You can customize and extend it as needed for your production environment.

Feel free to contribute, report issues, or request features by opening an issue on the repository.