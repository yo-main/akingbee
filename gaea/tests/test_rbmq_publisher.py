from collections import namedtuple
from mock import Mock, call
import pika

from gaea.rbmq import RBMQPublisher

from tests.fixtures import MockRBMQConnectionManager


def raise_err(ex):
    raise ex


def test_rbmq_publisher():

    mocked_channel = Mock()
    conn_manager = MockRBMQConnectionManager(mocked_channel)
    rbmq = RBMQPublisher(connection_manager=conn_manager)

    rbmq.publish("key1", "1", {"padim": "padam"})
    assert mocked_channel.basic_publish.call_count == 1

    call_args = mocked_channel.basic_publish.call_args.kwargs
    assert call_args["body"] == '"1"'
    assert call_args["exchange"] == "akingbee.main_exchange"
    assert call_args["routing_key"] == "key1"
    assert "emitter" in call_args["properties"].headers
    assert "created_at" in call_args["properties"].headers
    assert "padim" in call_args["properties"].headers
