import email
from .constants import *


class Email:
    def __init__(self, headers, body):
        self.email = email.message.EmailMessage()

        self.parse_headers(headers)
        self.email.set_content(body)

    def parse_headers(self, headers):
        if any(f not in headers for f in MANDATORY_EMAIL_FIELDS):
            raise ValueError(
                f"One or more mandatory fields is missing: {headers}"
            )

        for field, value in headers.items():
            if field not in EMAIL_FIELDS:
                raise ValueError(f"{field} is not a correct in email header")

            self.email[field] = value
