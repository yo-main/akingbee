from collections import namedtuple
from mock import Mock, call
import pika

from gaea.rbmq import RBMQConsumer

from tests.fixtures import MockRBMQConnectionManager


method = namedtuple("method", "delivery_tag, routing_key")

def raise_err(ex):
    raise ex

def test_rbmq_consumer():

    mocked_channel = Mock()
    conn_manager = MockRBMQConnectionManager(mocked_channel)
    handlers = {
        "key_1": lambda x, y: True,
        "key_2": lambda x, y: True,
        "key_3": lambda x, y: False,
        "key_4": lambda x, y: True,
        "boom": lambda x, y: raise_err(pika.exceptions.StreamLostError),
    }
    rbmq = RBMQConsumer(handlers=handlers, queue="test", connection_manager=conn_manager)

    # send messages
    rbmq.process(channel=mocked_channel, method=method("1", "key_1"), properties=None, body=None)
    rbmq.process(channel=mocked_channel, method=method("2", "key_2"), properties=None, body=None)
    rbmq.process(channel=mocked_channel, method=method("pouet", "pouet"), properties=None, body=None)
    rbmq.process(channel=mocked_channel, method=method("3", "key_3"), properties=None, body=None)
    rbmq.process(channel=mocked_channel, method=method("4", "key_4"), properties=None, body=None)
    rbmq.process(channel=mocked_channel, method=method("boom", "boom"), properties=None, body=None)
    rbmq.process(channel=mocked_channel, method=method("4", "key_4"), properties=None, body=None)

    assert mocked_channel.basic_ack.mock_calls == [call("1"), call("2"), call("4"), call("4")]
    assert mocked_channel.basic_nack.mock_calls == [call("pouet", requeue=False), call("3"), call("boom", requeue=False)]