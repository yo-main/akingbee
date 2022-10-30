from typing import Protocol

from domains.bee.entities.apiary import ApiaryEntity
from domains.bee.entities.vo.reference import Reference


class ApiaryRepositoryAdapter(Protocol):
    async def save_async(self, apiary: ApiaryEntity) -> None:
        ...

    async def get_async(self, reference: Reference) -> ApiaryEntity:
        ...
