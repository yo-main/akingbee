import asyncio
import pytest

from aristaeus.dispatcher import Dispatcher


class Registry:
    _registry: list = []

    @classmethod
    def call(cls, name):
        cls._registry.append(name)

    @classmethod
    def retrieve(cls):
        output = cls._registry
        cls._registry = []
        return output


@Dispatcher.subscribe("test.hello")
def coucou():
    Registry.call("hello")


@Dispatcher.subscribe("test.world")
async def world(cool):
    Registry.call(cool)


@Dispatcher.subscribe("test.hello")
async def olleh():
    Registry.call("olleh")


async def test_dispatched_nominal():
    Dispatcher.init()
    Dispatcher.publish("test.hello")
    Dispatcher.publish("test.world", cool=True)

    await asyncio.sleep(0.1)
    assert Registry.retrieve() == ["hello", "olleh", True]


async def test_dispatcher__stop():
    Dispatcher.stop()
    Dispatcher.publish("test.hello")
    Dispatcher.publish("test.world", cool=True)

    await asyncio.sleep(0.1)
    assert Registry.retrieve() == []
