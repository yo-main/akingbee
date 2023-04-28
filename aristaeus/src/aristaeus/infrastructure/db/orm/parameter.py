from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import Table
from sqlalchemy import Uuid
from sqlalchemy import DateTime
from sqlalchemy import UniqueConstraint

from aristaeus.domain.entities.parameter import Parameter

from .base import mapper_registry

parameter_table = Table(
    "parameter",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("public_id", Uuid(as_uuid=True), unique=True, nullable=False),
    Column("organization_id", Uuid(as_uuid=True), nullable=False),
    Column("key", Text, nullable=False),
    Column("value", Text, nullable=False),
    Column("date_creation", DateTime, default=datetime.now, nullable=False),
    Column("date_modification", DateTime, default=datetime.now, onupdate=datetime.now, nullable=False),
    UniqueConstraint("key", "value", "organization_id"),
)

mapper_registry.map_imperatively(Parameter, parameter_table)
