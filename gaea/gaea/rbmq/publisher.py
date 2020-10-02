import datetime
import json
import pika

from gaea.config import CONFIG
from gaea.log import logger

from .base import RBMQClient

class RBMQPublisher(RBMQClient):
    def __init__(self, exchange=None):
        self.exchange = exchange
        self.connection = self.get_connection()
        self.setup()

    def __enter__(self):
        return self

    def __exit__(self, ext, tb, v):
        self.connection.close()

    def setup(self):
        channel = self.connection.channel()
        self.declare_exchange(channel=channel)
        channel.close()

    @staticmethod
    def _get_default_headers():
        return {
            "emitter": CONFIG.SERVICE_NAME,
            "creation_at": datetime.datetime.utcnow().isoformat(),
        }

    def publish(self, routing_key, content, headers=None):

        if headers is None:
            headers = {}
        headers.update(self._get_default_headers())
        properties = pika.BasicProperties(headers=headers)
        body = json.dumps(content, default=str)

        try:
            channel = self.connection.channel()

            channel.basic_publish(
                exchange=self.exchange,
                routing_key=routing_key,
                body=body,
                properties=properties,
            )
        except:
            logger.exception("Fail to publish message in rbmq", body=body, properties=properties, routing_key=routing_key)
            raise
        finally:
            channel.close()

