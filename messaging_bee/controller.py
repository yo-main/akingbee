import json

from common.log.logger import logger

from .email import Email
from .motor import EmailEngine
from .constants import EMAIL_ADDRESS_NO_REPLY, SENDER


def reset_password(raw):
    if raw["type"] != "message":
        return

    logger.info("Message received: reset password", raw_data=raw)

    # validation
    try:
        data = json.loads(raw["data"])
    except:
        logger.exception("Message could not be parsed", raw_data=raw)
        raise

    if "headers" not in data or "body" not in data:
        logger.error("Incorrect message for reset_email", data=raw)
        raise ValueError(f"Invalid message received for reset_email: {data}")

    data["headers"][SENDER] = EMAIL_ADDRESS_NO_REPLY

    logger.info("Preparing email to be sent", email=data)
    email = Email(**data)
    EmailEngine().send(email)
