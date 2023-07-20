import os

NODE_ENV = "development" #os.getenv("NODE_ENV")
CLIENT_ID = "AfO8JyqOwNtRMq-3X9jr583UkVF10hxeG9Ifku6354w4Xh6eNOSClKl_6lLGi8FEDxseWsDwd9TdmGFG" #os.getenv("CLIENT_ID")
CLIENT_SECRET = "EBv2wZGG1L46fHNC7AZJcq_De-OqJrEjRarQeBiLnHBIoILGiNfgphPnxrwMCNIVSj_xpMQed1bHpVMI" #os.getenv("CLIENT_SECRET")

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
