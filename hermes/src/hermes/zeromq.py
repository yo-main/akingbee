import zmq
from gaea.config import CONFIG
from gaea.log import logger


def listen(handler):
    context = zmq.Context()
    socket = context.Socket(zmq.SUB)
    socket.connect(f"tcp://*.{CONFIG.ZEROMQ_PORT}")
    socket.subscribe("")

    while True:
        event = socket.recv_multipart()
        try:
            handler(json.loads(event))
        except Exception as exc:
            logger.exception(f"Error happened while processing event: {exc}")
