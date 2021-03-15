import ssl
import smtplib

from gaea.log import logger
from gaea.config import CONFIG

from hermes.constants import SENDER, TO


class EmailEngine:
    open_connections = {}

    def close(self, emails=None):
        if emails is None:
            emails = list(self.open_connections.keys())
        elif isinstance(emails, str):
            emails = [emails]

        for email in emails:
            connection = self.open_connections.get(email)
            if connection is None:
                logger.info(f"No opened connection for {email}")
                continue

            connection.close()
            logger.info(f"Closed connection for {email}")
            del self.open_connections[email]

    def get_email_client(self):
        return smtplib.SMTP_SSL(
            host=CONFIG.EMAIL_SERVER_HOST,
            port=CONFIG.EMAIL_SERVER_PORT,
            context=ssl.SSLContext(),
        )

    def login(self, email_address):
        if email_address in self.open_connections:
            return

        password_var_name = "{name}_EMAIL_PASSWORD".format(
            name=email_address.split("@")[0].upper()
        )

        password = CONFIG.get(password_var_name)
        if password is None:
            logger.error(f"Trying to connect to an unknown email: {email_address}")
            raise ValueError(f"{email_address} is unknown")

        client = self.get_email_client()
        client.login(email_address, password)
        logger.info(f"Connected to {email_address}")

        self.open_connections[email_address] = client

    def send(self, message):
        sender = message.email[SENDER]
        if sender not in self.open_connections:
            self.login(sender)

        client = self.open_connections[sender]
        client.send_message(message.email)

        logger.info(f"Email sent to {message.email[TO]}", email=message.email)
