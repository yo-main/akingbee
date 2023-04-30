from uuid import UUID

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from aristaeus.domain.adapters.repositories.user import UserRepositoryAdapter
from aristaeus.domain.entities.user import UserEntity
from aristaeus.domain.errors import EntityNotFound
from aristaeus.infrastructure.db import orm
from aristaeus.infrastructure.db.utils import error_handler
from aristaeus.injector import Injector

from .base import BaseRepository


@Injector.bind(UserRepositoryAdapter, "test")
class FakeUserRepository(BaseRepository):
    _users: set[UserEntity] = set()

    def __init__(self, session):
        self.session = session

    async def get(self, public_id: UUID) -> UserEntity:
        try:
            return next(user for user in self._users if user.public_id == public_id)
        except StopIteration:
            raise EntityNotFound("User not found")

    async def save(self, user: UserEntity) -> None:
        self._users.add(user)


@Injector.bind(UserRepositoryAdapter)
class UserRepository(BaseRepository):
    @error_handler
    async def get(self, public_id: UUID) -> UserEntity:
        query = select(UserEntity).where(orm.user_table.c.public_id == public_id)
        result = await self.session.execute(query)
        obj = result.scalar_one()
        return obj

    @error_handler
    async def save(self, user: UserEntity) -> None:
        data = {
            "public_id": user.public_id,
            "organization_id": user.organization_id,
        }
        query = insert(orm.user_table).values(data).on_conflict_do_nothing()

        await self.session.execute(query)
