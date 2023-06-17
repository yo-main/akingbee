import asyncio
import uuid

from aristaeus.controllers.consumers.app import zeromq_handler
from aristaeus.dispatcher import Dispatcher
from aristaeus.domain.services.unit_of_work import UnitOfWork


class FakeDeliver:
    def __init__(self, routing_key):
        self.routing_key = routing_key


async def test_user_created():
    Dispatcher.init()

    user_id = str(uuid.uuid4())
    payload = {
        "routing_key": "user.created",
        "body": {
            "user": {
                "id": user_id,
                "username": "kikoo",
            },
            "language": "fr",
        },
    }

    await zeromq_handler(payload)

    await asyncio.sleep(0)

    async with UnitOfWork() as uow:
        user = await uow.user.get(user_id)
        parameters = await uow.parameter.list(organization_id=user.organization_id)

    assert user and str(user.public_id) == user_id
    assert len(parameters) == 21
