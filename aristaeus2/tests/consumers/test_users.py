import asyncio
import json
import uuid

from sqlalchemy import select

from aristaeus.controllers.consumers.app import handler
from aristaeus.infrastructure.db.models.parameter import ParameterModel
from aristaeus.infrastructure.db.models.user import UserModel
from aristaeus.dispatcher import Dispatcher


class FakeDeliver:
    def __init__(self, routing_key):
        self.routing_key = routing_key


async def test_user_created(session):
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

    await asyncio.sleep(0.1)
    result = await session.execute(select(UserModel).where(UserModel.public_id == user_id))
    user = result.scalar()
    assert user and str(user.public_id) == user_id

    result = await session.execute(select(ParameterModel).where(ParameterModel.organization_id == user.organization_id))
    parameters = result.scalars().all()
    assert len(parameters) == 17
