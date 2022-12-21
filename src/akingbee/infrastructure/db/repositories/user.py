from uuid import UUID

from sqlalchemy import insert, select

from akingbee.domains.aristaeus.adapters.repositories.user import UserRepositoryAdapter
from akingbee.domains.aristaeus.entities.user import UserEntity
from akingbee.infrastructure.db.engine import AsyncDatabase
from akingbee.infrastructure.db.models.user import UserModel
from akingbee.infrastructure.db.utils import error_handler, get_data_from_entity
from akingbee.injector import Injector


@Injector.bind(UserRepositoryAdapter)
class UserRespository:
    database: AsyncDatabase

    @error_handler
    async def get(self, public_id: UUID) -> UserEntity:
        query = select(UserModel).where(UserModel.public_id == public_id)
        result = await self.database.execute(query)
        return result.scalar_one().to_entity()

    @error_handler
    async def save(self, user: UserEntity) -> None:
        data = get_data_from_entity(user)
        query = insert(UserModel).values(data)
        await self.database.execute(query)
