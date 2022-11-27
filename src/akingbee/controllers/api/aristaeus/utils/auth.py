from uuid import UUID

from fastapi import HTTPException
from fastapi import Depends
from fastapi import Cookie

from akingbee.domains.aristaeus.entities.user import UserEntity
from akingbee.infrastructure.clients.http.cerbes import CerbesClientAsyncAdapter
from akingbee.domains.aristaeus.adapters.repositories.user import UserRepositoryAdapter

from akingbee.config import settings
from akingbee.injector import InjectorMixin
from akingbee.utils.singleton import SingletonMeta


class UserManager(InjectorMixin, metaclass=SingletonMeta):
    cerbes: CerbesClientAsyncAdapter
    user_repository: UserRepositoryAdapter

    async def validate_access_token(self, access_token) -> str | None:
        return await self.cerbes.validate(access_token)

    async def get_logged_in_user(self, access_token) -> UserEntity:
        if not access_token:
            raise HTTPException(status_code=401)

        user_id = await self.validate_access_token(access_token=access_token)

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid access token")

        user = await self.user_repository.get(UUID(user_id))

        return user


async def auth_user(access_token=Cookie(None)) -> UserEntity:
    return await UserManager().get_logged_in_user(access_token)
