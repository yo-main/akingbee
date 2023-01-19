import asyncio
import json
import logging

from pika.spec import Basic
from pika import BasicProperties

from aristaeus.config import settings
from aristaeus.controllers.consumers.rbmq import AsyncRabbitMQConsumer
from aristaeus.controllers.consumers.resources.users import on_user_created

logger = logging.getLogger(__name__)


def handler(basic_deliver: Basic.Deliver, properties: BasicProperties, body: bytes):
    content = json.loads(body.decode())
    routing_key = basic_deliver.routing_key

    match routing_key:
        case "user.created":
            asyncio.ensure_future(on_user_created(properties, content))
        case _:
            logger.warning("Unknown routing key: %s", routing_key)


def create_app():
    consumer = AsyncRabbitMQConsumer(
        exchange=settings.RBMQ_EXCHANGE,
        exchange_type=settings.RBMQ_EXCHANGE_TYPE,
        queue=settings.RBMQ_QUEUE,
        callback=handler,
    )

    consumer.run()
