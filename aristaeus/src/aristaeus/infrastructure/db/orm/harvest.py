from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Table
from sqlalchemy import Text
from sqlalchemy import Uuid
from sqlalchemy.orm import relationship

from aristaeus.domain.entities.harvest import Harvest
from aristaeus.domain.entities.hive import Hive

from .base import mapper_registry

harvest_table = Table(
    "harvest",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("quantity", Integer, nullable=False),
    Column("apiary_name", Text, nullable=False),
    Column("hive_id", Integer, ForeignKey("hive.id"), nullable=False),
    Column("date_creation", DateTime, default=datetime.now, nullable=False),
    Column("date_modification", DateTime, default=datetime.now, onupdate=datetime.now, nullable=False),
)


mapper_registry.map_imperatively(
    Harvest,
    harvest_table,
    properties={
        "hive": relationship(Hive, lazy="joined", back_populates="harvests"),
    },
)
