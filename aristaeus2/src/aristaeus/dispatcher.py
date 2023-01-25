import asyncio
import logging
from typing import Any
from typing import Callable

logger = logging.getLogger(__name__)


class Dispatcher:

    _registry: dict[str, Any] = {}
    _queue: asyncio.Queue = asyncio.Queue()
    _started: bool = False

    @classmethod
    def publish(cls, key: str, **kwargs) -> None:
        if key not in cls._registry:
            logger.warning(f"No callback found for key {key}")
            return

        cls._queue.put_nowait((key, kwargs))

    @classmethod
    def subscribe(cls, key: str):
        def decorator(function: Callable):
            def wrapped_function(*args, **kwargs):
                return function(*args, **kwargs)

            cls._registry[key].append(function)
            return wrapped_function

        if key not in cls._registry:
            cls._registry[key] = []

        return decorator

    @classmethod
    def init(cls):
        if cls._started is False:
            cls._started = True
            return asyncio.ensure_future(cls.consume())

    @classmethod
    def stop(cls):
        cls._queue.put_nowait("terminate")
        cls._started = False

    @classmethod
    async def consume(cls):
        while True:
            msg = await cls._queue.get()

            if msg == "terminate":
                logger.info("Dispatcher's consumer terminated")
                break

            key, kwargs = msg

            callbacks = cls._registry[key]
            for callback in callbacks:
                if asyncio.iscoroutinefunction(callback):
                    await callback(**kwargs)
                else:
                    callback(**kwargs)
