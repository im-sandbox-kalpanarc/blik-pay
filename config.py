import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

NODE_ENV = os.getenv("NODE_ENV")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

isProd = NODE_ENV == "development"

PAYPAL_API_BASE = "https://api.paypal.com" if isProd else "https://api.sandbox.paypal.com"

# You can use these variables in your Python code as needed.
# For example:
if isProd:
    print("Running in production environment")
else:
    print("Running in sandbox environment")

print("PAYPAL_API_BASE:", PAYPAL_API_BASE)
print("CLIENT_ID:", CLIENT_ID)
print("CLIENT_SECRET:", CLIENT_SECRET)
