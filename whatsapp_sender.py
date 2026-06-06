import requests
import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv(
    "WHATSAPP_TOKEN"
)

PHONE_ID = os.getenv(
    "PHONE_NUMBER_ID"
)


def upload_media(image_path):

    url = (
        f"https://graph.facebook.com/v23.0/"
        f"{PHONE_ID}/media"
    )

    headers = {
        "Authorization":
        f"Bearer {TOKEN}"
    }

    files = {
        "file": (
            "poster.png",
            open(image_path, "rb"),
            "image/png"
        )
}

    data = {
        "messaging_product":
        "whatsapp"
    }

    response = requests.post(
        url,
        headers=headers,
        files=files,
        data=data
    )

    print("Status:", response.status_code)
    print("Response:", response.text)
    print("Size:", os.path.getsize(image_path))

    print("TOKEN START:", TOKEN[:20])
    print("PHONE ID:", PHONE_ID)
    print("URL:", url)

    result = response.json()

    if "id" not in result:
        raise Exception(result)

    return result["id"]


def send_image(
        phone,
        image_path
):
    print("Image path:", image_path)
    print("Image exists?", os.path.exists(image_path))

    media_id = upload_media(
        image_path
    )

    url = (
        f"https://graph.facebook.com/v23.0/"
        f"{PHONE_ID}/messages"
    )

    headers = {
        "Authorization":
        f"Bearer {TOKEN}",
        "Content-Type":
        "application/json"
    }

    print("TOKEN START:", TOKEN[:20])
    print("PHONE ID:", PHONE_ID)
    print("URL:", url)

    payload = {

        "messaging_product":
        "whatsapp",

        "to":
        phone,

        "type":
        "image",

        "image": {
            "id":
            media_id,

            "caption":
            "🎉 Happy Birthday 🎉"
        }
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload
    )

    print("SEND STATUS:", response.status_code)
    print("SEND RESPONSE:", response.text)