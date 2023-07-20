import requests
import base64
from config import PAYPAL_API_BASE, CLIENT_ID, CLIENT_SECRET

def get_access_token():
    credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
    credentials_base64 = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Accept": "application/json",
        "Authorization": f"Basic {credentials_base64}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {
        "grant_type": "client_credentials",
    }

    response = requests.post(f"{PAYPAL_API_BASE}/v1/oauth2/token", headers=headers, data=data)
    response.raise_for_status()

    return response.json()

if __name__ == "__main__":
    access_token = get_access_token()
    print("Access Token:", access_token)
