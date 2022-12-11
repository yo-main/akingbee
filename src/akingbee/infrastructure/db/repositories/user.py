import asyncio
import functools
from typing import TYPE_CHECKING, Protocol
from uuid import UUID

from sqlalchemy import select

from akingbee.domains.aristaeus.adapters.repositories.user import UserRepositoryAdapter
from akingbee.domains.aristaeus.entities.user import UserEntity
from akingbee.domains.aristaeus.errors import EntitySavingError
from akingbee.infrastructure.db.engine import AsyncDatabase
from akingbee.infrastructure.db.models.user import UserModel
from akingbee.infrastructure.db.utils import error_handler
from akingbee.injector import Injector


@Injector.bind(UserRepositoryAdapter)
class UserRespository:
    database: AsyncDatabase

    @error_handler
    async def get(self, public_id: UUID) -> UserEntity:
        query = select(UserModel).where(UserModel.public_id == public_id)
        async with self.database.get_session() as session:
            result = await session.scalar(query)
        return result.to_entity()

    @error_handler
    async def save(self, entity: UserEntity) -> None:
        model = UserModel.from_entity(entity)
        await self.database.save(model)
