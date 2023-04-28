from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import Table
from sqlalchemy import Uuid
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from aristaeus.domain.entities.comment import Comment
from aristaeus.domain.entities.hive import Hive
from aristaeus.domain.entities.event import Event

from .base import mapper_registry

comment_table = Table(
    "comment",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("public_id", Uuid(as_uuid=True), unique=True, nullable=False),
    Column("hive_id", Integer, ForeignKey("hive.id"), nullable=False),
    Column("event_id", Integer, ForeignKey("event.id"), nullable=True),
    Column("date", DateTime, nullable=False),
    Column("body", Text, nullable=False),
    Column("type", Text, nullable=False),
    Column("date_creation", DateTime, default=datetime.now, nullable=False),
    Column("date_modification", DateTime, default=datetime.now, onupdate=datetime.now, nullable=False),
)

mapper_registry.map_imperatively(
    Comment,
    comment_table,
    properties={
        "hive": relationship(Hive, lazy="joined"),
        "event": relationship(Event, lazy="joined"),
    },
)
