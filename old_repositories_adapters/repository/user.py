from typing import Protocol
from typing import TYPE_CHECKING

from akingbee.domains.aristaeus.entities.user import UserEntity
from akingbee.domains.aristaeus.entities.vo.reference import Reference

if TYPE_CHECKING:
    Base = object
else:
    Base = Protocol


class UserRepositoryAdapterAsync(base):
    async def save(self, user: UserEntity) -> None:
        ...

    async def get(self, reference: Reference) -> UserEntity:
        ...
