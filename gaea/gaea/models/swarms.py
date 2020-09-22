import datetime
import uuid

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import TIMESTAMP, TEXT, BYTEA, UUID

from .base import Base
from .users import Users


class SwarmHealthStatuses(Base):
    __tablename__ = "swarm_health_statuses"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(TEXT())
    user_id = Column(UUID(as_uuid=True), ForeignKey(Users.id), nullable=False)

    created_at = Column(TIMESTAMP(), default=datetime.datetime.utcnow)
    updated_at = Column(
        TIMESTAMP(), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )
    deleted_at = Column(TIMESTAMP(), nullable=True)

    user = relationship(Users, backref="swarm_healths")


class Swarms(Base):
    __tablename__ = "swarms"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    health_status_id = Column(
        UUID(as_uuid=True), ForeignKey(SwarmHealthStatuses.id), nullable=False
    )
    user_id = Column(UUID(as_uuid=True), ForeignKey(Users.id), nullable=False)

    created_at = Column(TIMESTAMP(), default=datetime.datetime.utcnow)
    updated_at = Column(
        TIMESTAMP(), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )
    deleted_at = Column(TIMESTAMP(), nullable=True)

    user = relationship(Users, backref="swarms_healths")
    health = relationship(SwarmHealthStatuses)
