import requests
import os

TOKEN = os.getenv("WHATSAPP_TOKEN")

response = requests.get(
    "https://graph.facebook.com/v23.0/me",
    headers={
        "Authorization": f"Bearer {TOKEN}"
    }
)

print(response.status_code)
print(response.text)