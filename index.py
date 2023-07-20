import os
import requests
from flask import Flask, request, jsonify, render_template
from pathlib import Path
import webbrowser

app = Flask(__name__)
app = Flask(__name__, static_url_path="/static", static_folder="client")

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

PAYPAL_API_BASE = "https://api.paypal.com"
WEBHOOK_ID = "YOUR_WEBHOOK_ID"  # Replace with your actual webhook ID

@app.route("/")
def index():
    index_path = Path(__file__).parent.parent / "client" / "index.html"
    return render_template("index.html")

@app.route("/capture/<string:orderId>", methods=["POST"])
def capture_order(orderId):
    access_token = get_access_token()

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    url = f"{PAYPAL_API_BASE}/v2/checkout/orders/{orderId}/capture"

    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        print("💰 Payment captured!")
        return response.json()
    except requests.exceptions.RequestException as e:
        print("❌ Payment failed.")
        return jsonify({"error": "Payment failed"}), 400

@app.route("/webhook", methods=["POST"])
def webhook():
    access_token = get_access_token()

    event_type = request.json["event_type"]
    resource = request.json["resource"]
    orderId = resource["id"]

    print("🪝 Received Webhook Event")

    # Verify the webhook signature
    try:
        verify_webhook_signature(access_token, request.headers, request.json)
    except requests.exceptions.RequestException as e:
        print("⚠️ Webhook signature verification failed.")
        return jsonify({"error": "Webhook signature verification failed"}), 400

    # Capture the order
    if event_type == "CHECKOUT.ORDER.APPROVED":
        try:
            capture_order(orderId, access_token)
        except requests.exceptions.RequestException as e:
            print("❌ Payment failed.")
            return jsonify({"error": "Payment failed"}), 400

    return "", 200

def get_access_token():
    # Replace these with your actual CLIENT_ID and CLIENT_SECRET
    CLIENT_ID = "AfO8JyqOwNtRMq-3X9jr583UkVF10hxeG9Ifku6354w4Xh6eNOSClKl_6lLGi8FEDxseWsDwd9TdmGFG" #os.environ.get("CLIENT_ID")
    CLIENT_SECRET = "EBv2wZGG1L46fHNC7AZJcq_De-OqJrEjRarQeBiLnHBIoILGiNfgphPnxrwMCNIVSj_xpMQed1bHpVMI" #os.environ.get("CLIENT_SECRET")

    data = {
        "grant_type": "client_credentials",
    }

    response = requests.post(
        f"{PAYPAL_API_BASE}/v1/oauth2/token",
        auth=(CLIENT_ID, CLIENT_SECRET),
        data=data
    )

    response.raise_for_status()

    return response.json()["access_token"]

def verify_webhook_signature(access_token, headers, body):
    headers["Authorization"] = f"Bearer {access_token}"

    url = f"{PAYPAL_API_BASE}/v1/notifications/verify-webhook-signature"

    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()

    verification_status = response.json()["verification_status"]
    if verification_status != "SUCCESS":
        raise requests.exceptions.RequestException()

def capture_order(orderId, access_token):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    url = f"{PAYPAL_API_BASE}/v2/checkout/orders/{orderId}/capture"

    response = requests.post(url, headers=headers)
    response.raise_for_status()

    print("💰 Payment captured!")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    webbrowser.open(f"http://localhost:{port}")
    app.run(host="0.0.0.0", port=port)
