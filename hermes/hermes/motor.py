import os
import ssl
import smtplib

from common.log.logger import logger
from common.config import CONFIG

from .constants import *


class EmailEngine:
    def __init__(self):
        self.ssl_context = ssl.SSLContext()
        self.client = self.get_email_client()
        self.logged = False

    def close(self):
        self.client.close()
        self.logged = False
        logger.info(f"Closed connection to {self.client.user}")

    def get_email_client(self):
        return smtplib.SMTP_SSL(
            host=EMAIL_SERVER_HOST,
            port=EMAIL_SERVER_PORT,
            context=self.ssl_context,
        )

    def login(self, email_address):
        password_attr = "{name}_EMAIL_PASSWORD".format(
            name=email_address.split("@")[0].upper()
        )

        if not hasattr(CONFIG, password_attr):
            logger.error(
                f"Trying to connect to an unknown email: {email_address}"
            )
            raise ValueError(f"{email_address} is unknown")

        password = getattr(CONFIG, password_attr)

        self.client.login(email_address, password)
        self.logged = True
        logger.info(f"Connected to {email_address}")

    def send(self, message):
        if not self.logged:
            self.login(message.email[SENDER])
            self.client.send_message(message.email)
            self.close()
        else:
            self.client.send_message(message.email)

        logger.info(f"Email sent to {message.email[TO]}", email=message.email)
