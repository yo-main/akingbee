import json

from gaea.log import logger
from gaea.config import CONFIG

from hermes.constants import SENDER
from hermes.email_engine import EmailEngine
from hermes.email_engine.email import Email
from hermes.templates.welcome_email import CONTENT as WELCOME_EMAIL
from hermes.templates.reset_password import CONTENT as RESET_PASSWORD_EMAIL


def welcome_new_user(properties, payload):
    logger.info(
        "Received message to welcome a new user !",
        properties=properties,
        payload=payload,
    )

    try:
        payload = json.loads(payload)
    except:
        logger.exception("Message is not in JSON format")
        return False

    required_keys = ("user", "language", "activation_link")

    if any(key not in payload for key in required_keys):
        logger.error(
            "Incorrect message received - some keys are missing", payload=payload
        )
        return False

    send_email(payload, WELCOME_EMAIL, activation_link=payload["activation_link"])


def reset_user_password(properties, payload):
    logger.info(
        "Received message to reset a user password !",
        properties=properties,
        payload=payload,
    )

    try:
        payload = json.loads(payload)
    except:
        logger.exception("Message is not in JSON format")
        return False

    required_keys = ("user", "language", "reset_link")

    if any(key not in payload for key in required_keys):
        logger.error(
            "Incorrect message received - some keys are missing", payload=payload
        )
        return False

    send_email(payload, RESET_PASSWORD_EMAIL, reset_link=payload["reset_link"])


def send_email(payload, template, **kwargs):
    language = payload["language"]
    receiver = payload["user"]["email"]
    sender = CONFIG.NOREPLY_EMAIL

    subject = template[language]["subject"]
    body = template[language]["body"].format(**kwargs)

    email = Email(sender=sender, receiver=receiver, subject=subject, body=body)

    client = EmailEngine()
    client.send(email)
    logger.info("Email sent !", payload=payload, subject=subject)
    client.close()
