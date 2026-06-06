import os
import json
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

from google.oauth2 import service_account

import io
import re

from httplib2 import Credentials


SCOPES = [
    "https://www.googleapis.com/auth/drive"
]


def extract_file_id(url):

    patterns = [
        r"/d/([^/]+)",
        r"id=([^&]+)"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            url
        )

        if match:
            return match.group(1)

    return None


def download_photo(
        drive_url,
        output_file
):

    file_id = extract_file_id(
        drive_url
    )

    scope = [
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/spreadsheets"
    ]

    if os.path.exists("credentials.json"):
        # Local development
        creds = Credentials.from_service_account_file(
            "credentials.json",
            scopes=scope
        )
    else:
        # Render deployment
        creds_dict = json.loads(
            os.environ["GOOGLE_CREDS"]
        )

        creds = Credentials.from_service_account_info(
            creds_dict,
            scopes=scope
        )

    service = build(
        "drive",
        "v3",
        credentials=creds
    )

    request = service.files().get_media(
        fileId=file_id
    )

    file = io.BytesIO()

    downloader = MediaIoBaseDownload(
        file,
        request
    )

    done = False

    while not done:

        status, done = downloader.next_chunk()

    with open(
        output_file,
        "wb"
    ) as f:

        f.write(
            file.getvalue()
        )

    return output_file