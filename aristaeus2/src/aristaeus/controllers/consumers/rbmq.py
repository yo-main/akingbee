import asyncio
import logging
from typing import Callable

from pika import ConnectionParameters, PlainCredentials, URLParameters
from pika.adapters.asyncio_connection import AsyncioConnection

from aristaeus.config import settings

logging.basicConfig(level=logging.INFO)


logger = logging.getLogger(__name__)


class AsyncRabbitMQConsumer:
    def __init__(self, exchange: str, exchange_type: str, queue: str, callback: Callable, routing_keys: list[str]):
        self.exchange = exchange
        self.exchange_type = exchange_type
        self.queue = queue
        self.callback = callback
        self.routing_keys = list(routing_keys)

        self.should_reconnect = False
        self.was_consuming = False

        self._connection = None
        self._channel = None
        self._closing = False
        self._consumer_tag = None
        self._consuming = False
        self._prefetch_count = 5

    def connect(self):
        """
        This method connects to RabbitMQ, returning the connection handle.
        When the connection is established, the on_connection_open method will be invoked by pika.
        """
        credentials = PlainCredentials(settings.rbmq_user, settings.rbmq_password)
        return AsyncioConnection(
            parameters=ConnectionParameters(
                host=settings.rbmq_host,
                port=settings.rbmq_port,
                virtual_host=settings.rbmq_vhost,
                credentials=credentials,
            ),
            on_open_callback=self.on_connection_open,
            on_open_error_callback=self.on_connection_open_error,
        )

    def on_connection_open(self, _unused_connection):
        """
        This method is called by pika once the connection to RabbitMQ has been established.
        It passes the handle to the connection object in case we need it, but in this case, we'll just mark it unused.
        """
        logger.info("Rabbitmq connection opened")
        self.open_channel()

    def on_connection_open_error(self, _unused_connection, err):
        """
        This method is called by pika if the connection to RabbitMQ can't be established.
        """
        logger.error("Rabbitmq Connection open failed: %s", err)
        self.reconnect()

    def reconnect(self):
        """
        Will be invoked if the connection can't be opened or is closed.
        Indicates that a reconnect is necessary then stops the ioloop.
        """
        self.should_reconnect = True
        self.stop()

    def open_channel(self):
        """
        Open a new channel with RabbitMQ by issuing the Channel.Open RPC command.
        When RabbitMQ responds that the channel is open, the on_channel_open callback will be invoked by pika.
        """
        logger.info("Creating a new channel")
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        """
        This method is invoked by pika when the channel has been opened.
        The channel object is passed in so we can make use of it.
        Since the channel is now open, we'll declare the exchange to use.
        """
        logger.info("Channel opened")
        self._channel = channel
        self._channel.add_on_close_callback(self.on_channel_closed)

        self.setup_exchange()

    def on_channel_closed(self, channel, reason):
        """
        Invoked by pika when RabbitMQ unexpectedly closes the channel. Channels are usually closed if you attempt to do
        something that violates the protocol, such as re-declare an exchange or queue with different parameters.
        In this case, we'll close the connection to shutdown the object.
        """
        logger.warning("Channel %i was closed: %s", channel, reason)
        self.close_connection()

    def close_connection(self):
        self._consuming = False
        if self._connection.is_closing or self._connection.is_closed:
            logger.info("Connection is closing or already closed")
        else:
            logger.info("Closing connection")
            self._connection.close()

    def setup_exchange(self):
        """
        Setup the exchange on RabbitMQ by invoking the Exchange.Declare RPC command. When it is complete,
        the on_exchange declareok method will be invoked by pika.
        """
        logger.info("Declaring exchange: %s", self.exchange)
        self._channel.exchange_declare(
            exchange=self.exchange, exchange_type=self.exchange_type, callback=self.on_exchange_declareok, durable=True
        )

    def on_exchange_declareok(self, _unused_frame):
        """
        Invoked by pika when RabbitMQ has finished the Exchange.Declare RPC command.
        """
        logger.info("Exchange declared: %s", self.exchange)
        self.setup_queue()

    def setup_queue(self):
        """
        Setup the queue on RabbitMQ by invoking the Queue.Declare RPC command. When it is complete,
        the on_queue_declareok method will be invoked by pika.
        """
        logger.info("Declaring queue %s", self.queue)
        self._channel.queue_declare(queue=self.queue, callback=self.on_queue_declareok)

    def on_queue_declareok(self, _unused_frame):
        """
        Method invoked by pika when the Queue.Declare RPC call made in setup_queue has completed. In this method we
        will bind the queue and exchange together with the routing key by issuing the Queue.Bind RPC command.
        When this command is complete, the on_bindok method will be invoked by pika.
        """
        logger.info("Binding %s to %s with %s", self.exchange, self.queue, self.routing_keys)
        for routing_key in self.routing_keys:
            self._channel.queue_bind(self.queue, self.exchange, routing_key=routing_key, callback=self.on_bindok)

    def on_bindok(self, _unused_frame):
        """
        Invoked by pika when the Queue.Bind method has completed. At this point we will set the prefetch count for the
        channel.
        """
        logger.info("Queue bound: %s", self.queue)
        self.set_qos()

    def set_qos(self):
        """
        This method sets up the consumer prefetch to only be delivered one message at a time. The consumer must
        acknowledge this message before RabbitMQ will deliver another one. You should experiment with different
        prefetch values to achieve desired performance.
        """
        self._channel.basic_qos(prefetch_count=self._prefetch_count, callback=self.on_basic_qos_ok)

    def on_basic_qos_ok(self, _unused_frame):
        """
        Invoked by pika when the Basic.QoS method has completed. At this point we will start consuming messages by
        calling start_consuming which will invoke the needed RPC commands to start the process.
        """
        logger.info("QOS set to: %d", self._prefetch_count)
        self.start_consuming()

    def start_consuming(self):
        """
        This method sets up the consumer by first calling add_on_cancel_callback so that the object is notified if
        RabbitMQ cancels the consumer. It then issues the Basic.Consume RPC command which returns the consumer tag that
        is used to uniquely identify the consumer with RabbitMQ. We keep the value to use it when we want to cancel
        consuming. The on_message method is passed in as a callback pika will invoke when a message is fully received.
        """
        logger.info("Issuing consumer related RPC commands")
        self.add_on_cancel_callback()
        self._consumer_tag = self._channel.basic_consume(self.queue, self.on_message)
        self.was_consuming = True
        self._consuming = True

    def add_on_cancel_callback(self):
        """
        Add a callback that will be invoked if RabbitMQ cancels the consumer for some reason. If RabbitMQ does cancel
        the consumer, on_consumer_cancelled will be invoked by pika.
        """
        logger.info("Adding consumer cancellation callback")
        self._channel.add_on_cancel_callback(self.on_consumer_cancelled)

    def on_consumer_cancelled(self, method_frame):
        """
        Invoked by pika when RabbitMQ sends a Basic.Cancel for a consumer receiving messages.
        """
        logger.info("Consumer was cancelled remotely, shutting down: %r", method_frame)
        if self._channel:
            self._channel.close()

    def on_message(self, _unused_channel, basic_deliver, properties, body):
        """
        Invoked by pika when a message is delivered from RabbitMQ. The channel is passed for your convenience.
        The basic_deliver object that is passed in carries the exchange, routing key, delivery tag and a redelivered
        flag for the message. The properties passed in is an instance of BasicProperties with the message properties
        and the body is the message that was sent.
        """
        logger.info("Received message # %s from %s: %s", basic_deliver.delivery_tag, properties.app_id, body)

        self.callback(basic_deliver, properties, body)
        self.acknowledge_message(basic_deliver.delivery_tag)

    def acknowledge_message(self, delivery_tag):
        """
        Acknowledge the message delivery from RabbitMQ by sending a Basic.Ack RPC method for the delivery tag.
        """
        logger.info("Acknowledging message %s", delivery_tag)
        self._channel.basic_ack(delivery_tag)

    def stop_consuming(self):
        """
        Tell RabbitMQ that you would like to stop consuming by sending the Basic.Cancel RPC command.
        """
        if self._channel:
            logger.info("Sending a Basic.Cancel RPC command to RabbitMQ")
            self._channel.basic_cancel(self._consumer_tag, self.on_cancelok)

    def on_cancelok(self, _unused_frame):
        """
        This method is invoked by pika when RabbitMQ acknowledges the cancellation of a consumer. At this point we will
        close the channel. This will invoke the on_channel_closed method once the channel has been closed, which will
        in-turn close the connection.
        """
        self._consuming = False
        logger.info("RabbitMQ acknowledged the cancellation of the consumer: %s", self._consumer_tag)
        self.close_channel()

    def close_channel(self):
        """
        Call to close the channel with RabbitMQ cleanly by issuing the Channel.Close RPC command.
        """
        logger.info("Closing the channel")
        self._channel.close()

    def run(self):
        """
        Run the example consumer by connecting to RabbitMQ and then starting the IOLoop to block and allow the
        AsyncioConnection to operate.
        """
        self._connection = self.connect()
        self._connection.ioloop.run_forever()

    def stop(self):
        """
        Cleanly shutdown the connection to RabbitMQ by stopping the consumer with RabbitMQ. When RabbitMQ confirms the
        cancellation, on_cancelok will be invoked by pika, which will then closing the channel and connection.
        The IOLoop is started again because this method is invoked when CTRL-C is pressed raising a KeyboardInterrupt
        exception. This exception stops the IOLoop which needs to be running for pika to communicate with RabbitMQ.
        All of the commands issued prior to starting the IOLoop will be buffered but not processed.
        """
        if not self._closing:
            self._closing = True
            logger.info("Stopping")
            if self._consuming:
                self.stop_consuming()
                self._connection.ioloop.run_forever()
            else:
                self._connection.ioloop.stop()
            logger.info("Stopped")
