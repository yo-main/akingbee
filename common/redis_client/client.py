import os
import redis

from common.log.logger import logger

from .messages import check_channel


class RedisClient:
    def __init__(self):
        self.client = self.get_client()
        self.pubsub = self.client.pubsub()

    def get_client(self):
        return redis.Redis(host=os.environ.get("REDIS_HOST", "localhost"))

    def publish(self, channel, message):
        if not check_channel(channel):
            logger.error(f"Channel `{channel}` is unknown")
        self.client.publish(channel, message)

    def listen(self, channel, callback):
        self.pubsub.subscribe(channel)

        for msg in self.pubsub.listen():
            callback(msg)
