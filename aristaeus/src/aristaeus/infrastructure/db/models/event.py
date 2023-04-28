from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Table
from sqlalchemy import Text
from sqlalchemy import Uuid
from sqlalchemy.orm import relationship

from aristaeus.domain.entities.comment import CommentEntity
from aristaeus.domain.entities.event import EventEntity
from aristaeus.domain.entities.hive import HiveEntity

from .base import mapper_registry

event_table = Table(
    "event",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("public_id", Uuid(as_uuid=True), unique=True, nullable=False),
    Column("hive_id", Integer, ForeignKey("hive.id"), nullable=False),
    Column("title", Text, nullable=False),
    Column("description", Text, nullable=False),
    Column("due_date", DateTime, nullable=False),
    Column("status", Text, nullable=False),
    Column("type", Text, nullable=False),
    Column("date_creation", DateTime, default=datetime.now, nullable=False),
    Column("date_modification", DateTime, default=datetime.now, onupdate=datetime.now, nullable=False),
)

mapper_registry.map_imperatively(
    EventEntity,
    event_table,
    properties={
        "hive": relationship(HiveEntity, lazy="joined"),
        "comment": relationship(CommentEntity, lazy="joined"),
    },
)
