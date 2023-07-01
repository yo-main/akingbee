import asyncio
import json
import logging

from aristaeus.controllers.consumers import zeromq
from aristaeus.controllers.consumers.resources.users import on_user_created
from aristaeus.dispatcher import Dispatcher

logger = logging.getLogger(__name__)


ROUTING_KEYS = {
    "user.created": on_user_created,
}


async def zeromq_handler(event):
    routing_key = event["routing_key"]

    command = ROUTING_KEYS.get(routing_key)
    if command is None:
        logger.warning("Unknown routing key: %s", routing_key)
        return

    await command(json.loads(event["body"]))


async def create_app():
    Dispatcher.init()
    await zeromq.listen(zeromq_handler)


if __name__ == "__main__":
    asyncio.run(create_app())
