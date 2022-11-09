from typing import Protocol
from typing import TYPE_CHECKING

from akingbee.domains.aristaeus.entities.apiary import ApiaryEntity
from akingbee.domains.aristaeus.entities.vo.reference import Reference

if TYPE_CHECKING:
    Base = object
else:
    Base = Protocol


class ApiaryRepositoryAdapter(Base):
    async def save_async(self, apiary: ApiaryEntity) -> None:
        ...

    async def get_async(self, reference: Reference) -> ApiaryEntity:
        ...
