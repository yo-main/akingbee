from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Table
from sqlalchemy import Text
from sqlalchemy import Uuid
from sqlalchemy.orm import relationship

from aristaeus.domain.entities.hive import HiveEntity
from aristaeus.domain.entities.apiary import ApiaryEntity
from aristaeus.domain.entities.swarm import SwarmEntity

from .base import mapper_registry

hive_table = Table(
    "hive",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("name", Text, nullable=False),
    Column("condition", Text, nullable=False),
    Column("owner", Text, nullable=False),
    Column("organization_id", Uuid(as_uuid=True), nullable=False),
    Column("public_id", Uuid(as_uuid=True), unique=True, nullable=False),
    Column("swarm_id", Integer, ForeignKey("swarm.id", ondelete="SET NULL"), nullable=True),
    Column("apiary_id", Integer, ForeignKey("apiary.id"), nullable=True),
    Column("date_creation", DateTime, default=datetime.now, nullable=False),
    Column("date_modification", DateTime, default=datetime.now, onupdate=datetime.now, nullable=False),
)

mapper_registry.map_imperatively(
    HiveEntity, hive_table, properties={
        "apiary": relationship(ApiaryEntity, lazy="joined"),
        "swarm": relationship(SwarmEntity, lazy="joined"),
    }
)

