from gaea.log import logger
from gaea.rbmq import RBMQConsumer

from aristaeus.consumer.handlers import initialize_user

if __name__ == "__main__":
    handlers = {
        "user.created": initialize_user,
    }

    consumer = RBMQConsumer(handlers=handlers, queue="aristaeus-main-queue")

    logger.info("Starting consumer")
    consumer.consume()
