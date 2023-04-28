from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import Table
from sqlalchemy import Text
from sqlalchemy import Uuid
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.orm import column_property

from aristaeus.domain.entities.apiary import ApiaryEntity

from .base import mapper_registry
from .hive import hive_table

apiary_table = Table(
    "apiary",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("name", Text, nullable=False),
    Column("location", Text, nullable=False),
    Column("honey_kind", Text, nullable=False),
    Column("public_id", Uuid(as_uuid=True), unique=True, nullable=False),
    Column("organization_id", Uuid(as_uuid=True), nullable=False),
    Column("date_creation", DateTime, default=datetime.now, nullable=False),
    Column("date_modification", DateTime, default=datetime.now, onupdate=datetime.now, nullable=False),
)

mapper_registry.map_imperatively(
    ApiaryEntity,
    apiary_table,
    properties={
        "hive_count": column_property(
            select(func.count(hive_table.c.id))
            .where(hive_table.c.apiary_id == apiary_table.c.id)
            .correlate_except(hive_table)
            .scalar_subquery()
        ),
    },
)
