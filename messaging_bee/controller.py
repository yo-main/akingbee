import json

from common.log.logger import logger

from .email import Email
from .motor import EmailEngine
from .constants import EMAIL_ADDRESS_NO_REPLY, SENDER


def reset_email(raw):
    if raw["type"] != "message":
        return

    # validation
    try:
        data = json.loads(raw["data"])
        logger.info(f"received: {data}")
    except:
        logger.exception(f"Not a valid json data: {raw}")
        raise

    if "headers" not in data or "body" not in data:
        raise ValueError(f"Invalid message received for reset_email: {data}")

    data["headers"][SENDER] = EMAIL_ADDRESS_NO_REPLY

    email = Email(**data)
    EmailEngine().send(email)
