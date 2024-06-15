import uuid
from dataclasses import dataclass
from dataclasses import field
from typing import TypeVar
from uuid import UUID

from aristaeus.domain.entities.vo.event_status import EventStatus
from aristaeus.domain.entities.vo.event_type import EventType
from aristaeus.domain.entities.vo.honey_kind import HoneyKind
from aristaeus.domain.entities.vo.swarm_health import SwarmHealth

from .base import Entity

ParameterType = TypeVar(
    "ParameterType",
    HoneyKind,
    SwarmHealth,
    EventType,
    EventStatus,
)


@dataclass
class Parameter(Entity):
    key: str
    value: str
    organization_id: UUID
    public_id: UUID = field(default_factory=uuid.uuid4)

    def change_value(self, new_value):
        self.value = new_value

    @staticmethod
    def of(entity: ParameterType, organization_id: UUID) -> "Parameter":
        match entity.__class__.__name__:
            case "HiveCondition":
                key = "hive_condition"
            case "HoneyKind":
                key = "honey_kind"
            case "SwarmHealth":
                key = "swarm_health"
            case "EventType":
                key = "event_type"
            case "EventStatus":
                key = "event_status"
            case "Owner":
                key = "owner"
            case _:
                raise Exception("Unknown parameter type")

        return Parameter(
            key=key,
            value=entity.value,
            organization_id=organization_id,
        )

    def __repr__(self):
        return f"<Parameter {self.public_id}>"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Parameter):
            raise ValueError(f"{other} is not a Hive")
        return self.public_id == other.public_id

    def __hash__(self) -> int:
        return hash(self.public_id)
