import json
import zmq
from gaea.config import CONFIG
from gaea.log import logger


def listen(handler):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(f"tcp://0.0.0.0:{CONFIG.ZEROMQ_PORT}")
    socket.subscribe("")

    while True:
        events = socket.recv_multipart()
        for event in events:
            try:
                handler(json.loads(event))
            except Exception as exc:
                logger.exception(f"Error happened while processing event: {exc}")
