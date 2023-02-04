from gaea.log import logger
from gaea.rbmq.consumer import RBMQConsumer

from hermes.controller import welcome_new_user, reset_user_password

HANDLERS = {
    "user.created": welcome_new_user,
    "user.reset_password": reset_user_password,
}


if __name__ == "__main__":
    consumer = RBMQConsumer(handlers=HANDLERS, queue="hermes-main-queue")
    logger.info("Starting consumer !")
    consumer.consume()
