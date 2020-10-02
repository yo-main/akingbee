import pika

from gaea.config import CONFIG
from gaea.log import logger

RBMQ_DEFAULT_EXCHANGE = "akingbee.main_exchange"

class RBMQClient:
    exchange = None

    def declare_exchange(self, channel):
        self.exchange = self.exchange or RBMQ_DEFAULT_EXCHANGE
        channel.exchange_declare(
            exchange=self.exchange,
            exchange_type="topic",
            durable=True,
        )

    def get_connection(self):
        params = self.get_connection_parameters()
        connection = pika.BlockingConnection(parameters=params)
        return connection

    @staticmethod
    def get_connection_parameters():
        creds = pika.PlainCredentials(CONFIG.RBMQ_USER, CONFIG.RBMQ_PASSWORD)
        return pika.ConnectionParameters(
            host=CONFIG.RBMQ_HOST,
            port=CONFIG.RBMQ_PORT,
            virtual_host=CONFIG.RBMQ_VHOST,
            credentials=creds,
            blocked_connection_timeout=300,
        )
