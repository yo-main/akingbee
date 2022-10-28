import uuid
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from domains.bee.entities.hive import HiveEntity
from domains.bee.entities.vo.reference import Reference


@dataclass(slots=True)
class EventEntity:
    public_id: Reference
    hive: HiveEntity
    title: str
    description: str
    due_date: datetime
    type: str
    status: str

    @staticmethod
    def create(
        title: str,
        description: str,
        due_date: datetime,
        type: str,
        status: str,
        hive: HiveEntity,
    ) -> "EventEntity":
        return EventEntity(
            public_id=Reference.of(uuid.uuid4()),
            hive=hive,
            title=title,
            description=description,
            due_date=due_date,
            type=type,
            status=status,
        )
