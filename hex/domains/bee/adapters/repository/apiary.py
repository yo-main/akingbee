from typing import Protocol

from domains.bee.entities.apiary import ApiaryEntity
from domains.bee.entities.vo.reference import Reference


class ApiaryRepositoryAdapter(Protocol):
    def save(self, apiary: ApiaryEntity) -> None:
        ...

    def get(self, reference: Reference) -> ApiaryEntity:
        ...
