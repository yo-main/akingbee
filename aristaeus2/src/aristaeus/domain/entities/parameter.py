import uuid
from dataclasses import dataclass, field
from typing import TypeVar
from uuid import UUID

from aristaeus.domain.entities.vo.event_status import EventStatus
from aristaeus.domain.entities.vo.event_type import EventType
from aristaeus.domain.entities.vo.honey_type import HoneyType
from aristaeus.domain.entities.vo.swarm_health import SwarmHealth

from .base import Entity

ParameterType = TypeVar(
    "ParameterType",
    HoneyType,
    SwarmHealth,
    EventType,
    EventStatus,
)


@dataclass(frozen=True, slots=True)
class ParameterEntity(Entity):
    key: str
    value: str
    organization_id: UUID
    public_id: UUID = field(default_factory=uuid.uuid4)

    @staticmethod
    def of(entity: ParameterType, organization_id: UUID) -> "ParameterEntity":

        match entity.__class__.__name__:
            case "HiveCondition":
                key = "hive_condition"
            case "HoneyType":
                key = "honey_type"
            case "SwarmHealth":
                key = "swarm_health"
            case "EventType":
                key = "event_type"
            case "EventStatus":
                key = "event_status"
            case _:
                raise Exception("Unknown parameter type")

        return ParameterEntity(
            key=key,
            value=entity.value,
            organization_id=organization_id,
        )
