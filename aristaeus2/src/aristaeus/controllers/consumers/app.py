from gaea.rbmq import RBMQConsumer

from .resources.users import on_user_created


def create_app():
    handlers = {
        "user.created": on_user_created
    }
    consumer = RBMQConsumer(handlers=handlers, queue="aristaeus-main-queue")
    return consumer