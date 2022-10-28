import uuid
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from domains.bee.entities.vo.reference import Reference

from .apiary import ApiaryEntity
from .event import EventEntity
from .hive import HiveEntity
from .swarm import SwarmEntity


@dataclass(slots=True)
class CommentEntity:
    public_id: Reference

    date: datetime
    type: str  # choice
    body: str

    hive: HiveEntity
    event: EventEntity | None

    @staticmethod
    def create(
        date: datetime,
        body: str,
        type: str,
        hive: HiveEntity,
        event: EventEntity | None,
    ) -> "CommentEntity":
        return CommentEntity(
            public_id=Reference.of(uuid.uuid4()),
            date=date,
            body=body,
            type=type,
            hive=hive,
            event=event,
        )
