import json
import logging
import zmq
import zmq.asyncio

from aristaeus.config import settings

logger = logging.getLogger(__name__)


async def listen(handler):
    context = zmq.asyncio.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(f"tcp://*:{settings.zeromq_port}")
    socket.suibscribe("")

    while True:
        event = await socket.recv_multipart()
        try:
            await handler(json.loads(event))
        except Exception as exc:
            logger.exception(f"Error happened while processing event: {exc}")
