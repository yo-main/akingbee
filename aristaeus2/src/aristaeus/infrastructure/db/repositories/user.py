from uuid import UUID

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from aristaeus.domain.adapters.repositories.user import UserRepositoryAdapter
from aristaeus.domain.entities.user import UserEntity
from aristaeus.infrastructure.db.engine import AsyncDatabase
from aristaeus.infrastructure.db.models.user import UserModel
from aristaeus.infrastructure.db.utils import error_handler, get_data_from_entity
from aristaeus.injector import Injector


@Injector.bind(UserRepositoryAdapter)
class UserRespository:
    database: AsyncDatabase

    @error_handler
    async def get(self, public_id: UUID) -> UserEntity:
        query = select(UserModel).where(UserModel.public_id == public_id)
        result = await self.database.execute(query)
        return result.scalar_one().to_entity()

    @error_handler
    async def save(self, user: UserEntity, session: AsyncSession | None) -> None:
        data = get_data_from_entity(user)
        query = insert(UserModel).values(data)

        if session is not None:
            await session.execute(query)
        else:
            await self.database.execute(query)
