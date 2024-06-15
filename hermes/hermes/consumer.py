import json
from gaea.log import logger
from hermes.zeromq import listen

from hermes.controller import welcome_new_user, reset_user_password


HANDLERS = {
    "user.created": welcome_new_user,
    "user.reset_password": reset_user_password,
}


def handler(event):
    routing_key = event["routing_key"]

    command = HANDLERS.get(routing_key)
    if command is None:
        logger.warning("Unknown routing key: %s", routing_key)
        return

    command(json.loads(event["body"]))


if __name__ == "__main__":
    logger.info("Starting consumer !")
    listen(handler)
