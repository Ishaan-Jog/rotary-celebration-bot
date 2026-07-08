import asyncio
from datetime import datetime
import pandas as pd
import gspread
import os
import json
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
from google_drive import download_photo
from poster_generator import generate_poster
from whatsapp_sender import send_image

load_dotenv()

DEFAULT_RECIPIENT = os.getenv(
    "RECIPIENT_PHONE"
)

SHEET_NAME = os.getenv("SHEET_NAME")


def get_sheet_data():

    SCOPES = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    if os.path.exists("credentials.json"):
        creds = Credentials.from_service_account_file(
            "credentials.json",
            scopes=SCOPES
        )
    else:

        creds = Credentials.from_service_account_info(
            json.loads(
                os.environ["GOOGLE_CREDS"]
            ),
            scopes=SCOPES
        )

    client = gspread.authorize(creds)

    sheet = client.open(
        SHEET_NAME
    ).sheet1

    records = sheet.get_all_records()

    return pd.DataFrame(records)


def is_today(date_value):

    try:

        event_date = pd.to_datetime(
            date_value,
            format="%d/%m/%Y"
        )

        today = datetime.now()

        return (
            event_date.day == today.day
            and
            event_date.month == today.month
        )

    except Exception as e:

        print(
            f"Date parsing failed: {e}"
        )

        return False


def process_row(row, event_date):

    name = row[
        "What is the name of the person being celebrated?"
    ]
    name = name.strip().replace("Rtn. ", "")
    name = "Rtn. " + name

    event_type = row[
        "Select the event type"
    ]

    photo_url = row[
        "Please upload a photo of the person"
    ]

    print(
        f"Processing {name}"
    )

    photo_path = download_photo(
        photo_url,
        f"photos/{name}.jpg"
    )

    event_date = pd.to_datetime(
        event_date,
        dayfirst=True
    )

    png_file = generate_poster(
        event_type=row[
            "Select the event type"
        ],
        name=row[
            "What is the name of the person being celebrated?"
        ],
        date=event_date.strftime(
            "%d %B"
        ),
        photo_path=photo_path
    )

    send_image(
        DEFAULT_RECIPIENT,
        png_file
    )

    print(
        f"Sent poster for {name}"
    )


def main():

    os.makedirs(
        "photos",
        exist_ok=True
    )

    os.makedirs(
        "generated",
        exist_ok=True
    )

    print(
        "Checking today's events..."
    )

    df = get_sheet_data()

    if df.empty:

        print(
            "No responses found."
        )

        return

    for _, row in df.iterrows():

        event_date = row[
            "Enter the date of the event"
        ]

        if is_today(event_date):

            process_row(row, event_date)


if __name__ == "__main__":

    main()