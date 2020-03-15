import email

FIELDS = {
    "Subject": True,
    "From": True,
    "Sender": True,
    "Cc": False,
    "Bcc": False}

class Email:

    def __init__(self, headers, body):
        self.msg = email.message.EmailMessage()

        self.parse_headers(headers)
        self.msg.set_content(body)

    def parse_headers(self, headers):
        if not all(f in headers for f in FIELDS if FIELDS[f]):
            raise ValueError(
                f"One or more mandatory fields is missing: {headers}"
            )

        for field, value in headers.items():
            if field not in FIELDS:
                raise ValueError(
                    f"{field} is not a correct in email header"
                )

            self.msg[field] = value


