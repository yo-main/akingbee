import pika

from gaea.log import logger

from .base import RBMQClient

class RBMQConsumer(RBMQClient):
    def __init__(self, handlers, queue, exchange=None):
        self.handlers = handlers
        self.queue = queue
        self.exchange = exchange

        self.connection = self.get_connection()

    def setup(self, channel):
        self.declare_queue(channel=channel)
        self.declare_exchange(channel=channel)
        self.bind_queues(channel=channel)

    def declare_queue(self, channel):
        channel.queue_declare(queue=self.queue, durable=True)

    def bind_queues(self, channel):
        for routing_key in self.handlers:
            channel.queue_bind(queue=self.queue, exchange=self.exchange, routing_key=routing_key)

    def consume(self):
        while True:
            logger.info("Starting consuming...", queue=self.queue)
            try:
                channel = self.connection.channel()
                self.setup(channel)
                channel.basic_consume(queue=self.queue, on_message_callback=self.process)
                channel.start_consuming()
            except KeyboardInterrupt:
                channel.stop_consuming()
                self.connection.close()
                logger.info("Goodbye")
                return
            except pika.exceptions.StreamLostError:
                logger.warning("RBMQ connection stream has been lost. Trying to reconnect")
                continue
            except:
                logger.exception("Critical error on consumer")
                raise

    def process(self, channel, method, properties, body):
        logger.info("New message received", properties=properties, body=body, routing_key=method.routing_key)
        handler = self.handlers[method.routing_key]
        success = handler(properties, body)
        if success:
            channel.basic_ack(method.delivery_tag)
        else:
            channel.basic_nack(method.delivery_tag)

