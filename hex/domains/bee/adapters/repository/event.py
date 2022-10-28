from typing import Protocol

from domains.bee.entities.event import EventEntity
from domains.bee.entities.vo.reference import Reference


class EventRepositoryAdapter(Protocol):
    def save(self, entity: EventEntity) -> None:
        ...

    def get(self, reference: Reference) -> EventEntity:
        ...
