from uuid import UUID

from fastapi import Cookie
from fastapi import HTTPException

from aristaeus.domain.services.unit_of_work import UnitOfWork
from aristaeus.domain.entities.user import User
from aristaeus.infrastructure.clients.http.cerbes import CerbesClientAsyncAdapter
from aristaeus.injector import InjectorMixin
from aristaeus.utils.singleton import SingletonMeta


class UserManager(InjectorMixin, metaclass=SingletonMeta):
    cerbes: CerbesClientAsyncAdapter

    async def validate_access_token(self, access_token) -> str | None:
        return await self.cerbes.validate(access_token)

    async def get_logged_in_user(self, access_token) -> User:
        if not access_token:
            raise HTTPException(status_code=401)

        user_id = await self.validate_access_token(access_token=access_token)

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid access token")

        async with UnitOfWork() as uow:
            user = await uow.user.get(UUID(user_id))

        return user


async def auth_user(access_token=Cookie(None), language=Cookie(None)) -> User:
    user = await UserManager().get_logged_in_user(access_token)
    if language:
        user.language = language
    return user
