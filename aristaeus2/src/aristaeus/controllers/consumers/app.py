import asyncio
import json
import logging

from pika.spec import Basic
from pika import BasicProperties

from aristaeus.config import settings
from aristaeus.controllers.consumers.rbmq import AsyncRabbitMQConsumer
from aristaeus.controllers.consumers.resources.users import on_user_created
from aristaeus.dispatcher import Dispatcher

logger = logging.getLogger(__name__)


ROUTING_KEYS = {
    "user.created": on_user_created,
}


def handler(basic_deliver: Basic.Deliver, properties: BasicProperties, body: bytes):
    content = json.loads(body.decode())
    routing_key = basic_deliver.routing_key

    handler = ROUTING_KEYS.get(routing_key)

    if not handler:
        logger.warning("Unknown routing key: %s", routing_key)
    else:
        asyncio.ensure_future(handler(properties, content))


def create_app():
    Dispatcher.init()
    consumer = AsyncRabbitMQConsumer(
        exchange=settings.rbmq_exchange,
        exchange_type=settings.rbmq_exchange_type,
        queue=settings.rbmq_queue,
        routing_keys=ROUTING_KEYS.keys(),
        callback=handler,
    )

    consumer.run()


if __name__ == "__main__":
    create_app()