from typing import Protocol

from domains.bee.entities.user import UserEntity
from domains.bee.entities.vo.reference import Reference


class UserRepositoryAdapterAsync(Protocol):
    async def save(self, user: UserEntity) -> None:
        ...

    async def get(self, reference: Reference) -> UserEntity:
        ...
