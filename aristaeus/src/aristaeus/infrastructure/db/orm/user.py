from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import Table
from sqlalchemy import Uuid

from aristaeus.domain.entities.user import UserEntity

from .base import mapper_registry

user_table = Table(
    "user",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("public_id", Uuid(as_uuid=True), unique=True, nullable=False),
    Column("organization_id", Uuid(as_uuid=True), nullable=False),
    Column("date_creation", DateTime, default=datetime.now, nullable=False),
    Column("date_modification", DateTime, default=datetime.now, onupdate=datetime.now, nullable=False),
)


mapper_registry.map_imperatively(UserEntity, user_table)
