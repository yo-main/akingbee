from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import Table
from sqlalchemy import Uuid
from sqlalchemy import DateTime

from aristaeus.domain.entities.swarm import SwarmEntity

from .base import mapper_registry

swarm_table = Table(
    "swarm",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("public_id", Uuid(as_uuid=True), unique=True, nullable=False),
    Column("health", Text, nullable=False),
    Column("queen_year", Integer, nullable=False),
    Column("date_creation", DateTime, default=datetime.now, nullable=False),
    Column("date_modification", DateTime, default=datetime.now, onupdate=datetime.now, nullable=False),
)

mapper_registry.map_imperatively(SwarmEntity, swarm_table)
