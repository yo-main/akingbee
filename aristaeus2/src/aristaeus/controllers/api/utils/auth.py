from uuid import UUID

from fastapi import Cookie, Depends, HTTPException

from aristaeus.config import settings
from aristaeus.domain.adapters.repositories.user import UserRepositoryAdapter
from aristaeus.domain.entities.user import UserEntity
from aristaeus.infrastructure.clients.http.cerbes import CerbesClientAsyncAdapter
from aristaeus.injector import InjectorMixin
from aristaeus.utils.singleton import SingletonMeta


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

        print(user_id)
        user = await self.user_repository.get(UUID(user_id))
        print("NICEEEE")

        return user


async def auth_user(access_token=Cookie(None)) -> UserEntity:
    return await UserManager().get_logged_in_user(access_token)
