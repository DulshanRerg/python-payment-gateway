from flask import Flask, request, jsonify
from services.azampay_service import AzamPayService
import logging

gateway = Flask(__name__)
azampay = AzamPayService()

# Configure logging
logging.basicConfig(filename="logs/gateway.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

@gateway.route("/mno-checkout", methods=["POST"])
def mno_checkout():
    """
    Endpoint to handle payment initiation requests from the frontend application.
    Expected JSON payload (from Frontend):
    {
        "accountNumber": "sender's number",
        "amount": "1000",
        "currency": "TZS",
        "externalId": "TXN-12345",
        "provider": "Airtel",
        "additionalProperties": { ... } // optional
    }
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON payload received"}), 400
    
    account_number = data.get("accountNumber")
    amount = data.get("amount")
    external_id = data.get("externalId")
    provider = data.get("provider")

    if not all([account_number, amount, external_id, provider]):
        return jsonify({"error": "Missing required fields"}), 400

    response = azampay.mno_checkout(account_number, amount, external_id, provider)
    
    if response:
        return jsonify(response), 200
    else:
        return jsonify({"error": "Failed to initiate payment"}), 500

@gateway.route("/api/v1/Checkout/Callback", methods=["POST"])
def checkout_callback():
    """
    Callback endpoint to handle transaction completion notifications from AzamPay.
    
    AzamPay sends a POST request to this endpoint once a transaction is confirmed by the user.
    The expected JSON payload (Content-Type: gatewaylication/json) should follow this schema:
    
    {
      "additionalProperties": { ... } or null,   // Optional additional data.
      "amount": "string",                         // Required. The amount charged.
      "fspReferenceId": "string",                 // Optional. Reference ID from partner FSP.
      "message": "string",                        // Required. Transaction description.
      "msisdn": "string",                         // Required. The consumer's account number/MSISDN.
      "operator": "string",                       // Required. Allowed values: "Airtel", "Tigo", "Halopesa", "Azampesa", "Mpesa".
      "reference": "string",                      // Required. Transaction ID.
      "submerchantAcc": "string",                 // Optional. Reserved for future use.
      "transactionstatus": "string",              // Required. "success" or "failure".
      "utilityref": "string"                      // Required. ID that belongs to your application.
    }
    
    This endpoint must be always available. It validates the payload, logs the data, and then
    the gateway forwards it to the frontend app.
    """
    callback_data = request.get_json()
    if not callback_data:
        gateway.logger.error("Callback received with no JSON payload.")
        return jsonify({"error": "No JSON payload received."}), 400

    # List of required fields
    required_fields = ["amount", "message", "msisdn", "operator", "reference", "transactionstatus", "utilityref"]
    missing_fields = [field for field in required_fields if field not in callback_data or not callback_data[field]]
    if missing_fields:
        gateway.logger.error("Callback missing required fields: %s", ", ".join(missing_fields))
        return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

    # Validate operator
    allowed_operators = ["Airtel", "Tigo", "Halopesa", "Azampesa", "Mpesa"]
    if callback_data.get("operator") not in allowed_operators:
        gateway.logger.error("Invalid operator in callback: %s", callback_data.get("operator"))
        return jsonify({"error": f"Invalid operator: {callback_data.get('operator')}. Allowed values: {', '.join(allowed_operators)}"}), 400

    # Validate transactionstatus is either "success" or "failure"
    if callback_data.get("transactionstatus") not in ["success", "failure"]:
        gateway.logger.error("Invalid transaction status in callback: %s", callback_data.get("transactionstatus"))
        return jsonify({"error": "Invalid transaction status. Must be 'success' or 'failure'"}), 400

    # Log the callback data
    gateway.logger.info("Received AzamPay callback: %s", callback_data)

    # Forward the callback data to the Laravel application.
    forward_result = azampay.forward_callback(callback_data)
    if forward_result:
        return jsonify({
            "status": "success",
            "message": "Callback processed and forwarded successfully."
        }), 200
    else:
        return jsonify({
            "status": "error",
            "message": "Failed to forward callback to Laravel."
        }), 500
@gateway.route("/")
def home():
    return "Hello, If you want to use this Payment API - send us a email via dulshanrerg01@duck.com!"

if __name__ == "__main__":
    gateway.run(host="0.0.0.0", port=5000, debug=True)

