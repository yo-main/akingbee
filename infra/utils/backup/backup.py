#! /usr/bin/env python

import datetime
import os
import subprocess

from cryptography.fernet import Fernet

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2 import service_account

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/drive.metadata.readonly",
    "https://www.googleapis.com/auth/drive.file",
]
CREDENTIAL_FILE = os.path.join("tokens", os.environ.get("CREDENTIAL_FILE", "google-credentials.json"))


GOOGLE_APP_FOLDER_NAME = "akingbee"
GOOGLE_FOLDER_MIME_TYPE = "application/vnd.google-apps.folder"


def authenticate():
    credentials = service_account.Credentials.from_service_account_file(
        CREDENTIAL_FILE, scopes=SCOPES)

    return credentials


def upload(file):
    creds = authenticate()
    drive = build("drive", "v3", credentials=creds)

    backup_folder = get_folder(name="backup", drive=drive)

    # file = MediaFileUpload(file, mimetype="text/plain")
    metadata = {
        "name": file,
        "mimeType": "text/plain",
        "parents": [backup_folder.get("id")],
    }

    drive.files().create(media_body=file, body=metadata).execute()


def get_folder(name, drive=None):
    if drive is None:
        creds = authenticate()
        drive = build("drive", "v3", credentials=creds)

    metadata = {"name": name, "mimeType": GOOGLE_FOLDER_MIME_TYPE}
    query = f"name = '{name}' and trashed = false"

    if name != GOOGLE_APP_FOLDER_NAME:
        app_folder = get_folder(name=GOOGLE_APP_FOLDER_NAME, drive=drive).get("id")
        query += f" and '{app_folder}' in parents"

    results = drive.files().list(q=query, fields="files(id, name)").execute()
    if results["files"]:
        return results["files"][0]

    return create_folder(name=name, drive=drive)


def create_folder(name, drive=None):
    if drive is None:
        creds = authenticate()
        drive = build("drive", "v3", credentials=creds)

    metadata = {"name": name, "mimeType": GOOGLE_FOLDER_MIME_TYPE}

    if name != GOOGLE_APP_FOLDER_NAME:
        app_folder = get_folder(name=GOOGLE_APP_FOLDER_NAME, drive=drive).get("id")
        metadata["parents"] = [app_folder]

    res = drive.files().create(body=metadata, fields="id").execute()
    return res


def dump_database():
    name = f"BACKUP_AKINGBEE-{datetime.datetime.utcnow().isoformat()}.txt"
    commands = [
        "pg_dump",
        "--file",
        name,
    ]
    subprocess.run(
        commands, check=True
    )  # check=true ensure an exception is raised if the command fails
    return name


def encrypt(file):
    key = os.environ["APP_KEY"]
    fernet = Fernet(key)

    with open(file, "rb") as _file:
        original = _file.read()

    encrypted = fernet.encrypt(original)

    with open(file, "wb") as target:
        target.write(encrypted)

    return file


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    file = dump_database()
    encrypted = encrypt("here")
    upload(encrypted)


if __name__ == "__main__":
    main()
