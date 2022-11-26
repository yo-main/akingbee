from typing import Protocol
from typing import TYPE_CHECKING
from uuid import UUID

from akingbee.domains.aristaeus.entities.apiary import ApiaryEntity

if TYPE_CHECKING:
    Base = object
else:
    Base = Protocol


class ApiaryRepositoryAdapter(Base):
    async def save(self, apiary: ApiaryEntity) -> None:
        ...

    async def get(self, public_id: UUID) -> ApiaryEntity:
        ...
