import asyncio
import os

from datetime import datetime

import pandas as pd
import gspread

from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

from google_drive import download_photo
from template_renderer import render_template
from html_to_png import generate_png
from whatsapp_sender import send_image

load_dotenv()

DEFAULT_RECIPIENT = os.getenv(
    "RECIPIENT_PHONE"
)

SHEET_NAME = os.getenv("SHEET_NAME")


def get_sheet_data():

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "credentials.json",
        scope
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


def process_row(row):

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

    html_file = render_template(
        name=name,
        photo_path=photo_path,
        event_type=event_type
    )

    png_file = asyncio.run(
        generate_png(html_file)
    )

    send_image(
        DEFAULT_RECIPIENT,
        png_file
    )

    print(
        f"Sent poster for {name}"
    )


def main():

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

            process_row(row)


if __name__ == "__main__":

    main()