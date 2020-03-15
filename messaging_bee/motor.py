import os
import ssl
import smtplib

EMAIL_SERVER_HOST = "smtp.zoho.eu"
EMAIL_SERVER_PORT = 465

class EmailEngine:
    def __init__(self):
        self.ssl_context = ssl.SSLContext()
        self.client = self.get_email_client()

    def close(self):
        self.client.close()

    def get_email_client(self):
        return smtplib.SMTP_SSL(
            host=EMAIL_SERVER_HOST,
            port=EMAIL_SERVER_PORT,
            context=self.ssl_context
        )

    def login(self, email_address):
        password = os.environ.get(
            "{name.upper()}_EMAIL_ADDRESS"
            .format(name=email_address.split("@")[0])
        )

        if password is None:
            raise ValueError(f"{email_address} is unknown")

        self.client.login(email_address, password)

    def send(self, message):
        self.client.send_message(message)


