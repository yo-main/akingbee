import asyncio
import json
import uuid

from aristaeus.controllers.consumers.app import handler
from aristaeus.dispatcher import Dispatcher
from aristaeus.domain.adapters.repositories.user import UserRepositoryAdapter
from aristaeus.domain.adapters.repositories.parameter import ParameterRepositoryAdapter
from aristaeus.injector import Injector


class FakeDeliver:
    def __init__(self, routing_key):
        self.routing_key = routing_key


async def test_user_created():
    Dispatcher.init()

    user_id = str(uuid.uuid4())
    payload = json.dumps(
        {
            "user": {
                "id": user_id,
                "username": "kikoo",
            },
            "language": "fr",
        }
    )

    handler(FakeDeliver("user.created"), None, payload.encode())

    await asyncio.sleep(0.3)

    user = await Injector.get(UserRepositoryAdapter).get(user_id)
    assert user and str(user.public_id) == user_id

    parameters = await Injector.get(ParameterRepositoryAdapter).list(organization_id=user.organization_id)
    assert len(parameters) == 17
