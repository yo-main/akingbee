import datetime
import uuid

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import TIMESTAMP, TEXT, BYTEA, UUID

from .base import Base
from .users import Users
from .swarms import SwarmHealthStatuses, Swarms
from .apiaries import Apiaries
from .hives import Hives, HiveConditions
from .events import Events


class CommentTypes(Base):
    __tablename__ = "comment_types"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(TEXT(), nullable=False)

    created_at = Column(TIMESTAMP(), default=datetime.datetime.utcnow)
    updated_at = Column(
        TIMESTAMP(), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )
    deleted_at = Column(TIMESTAMP(), nullable=True)


class Comments(Base):
    __tablename__ = "comments"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    comment = Column(TEXT(), nullable=False)
    date = Column(TIMESTAMP(), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey(Users.id), nullable=False)
    type_id = Column(UUID(as_uuid=True), ForeignKey(CommentTypes.id), nullable=False)
    swarm_id = Column(UUID(as_uuid=True), ForeignKey(Swarms.id), nullable=True)
    hive_id = Column(UUID(as_uuid=True), ForeignKey(Hives.id), nullable=True)
    apiary_id = Column(UUID(as_uuid=True), ForeignKey(Apiaries.id), nullable=True)
    event_id = Column(UUID(as_uuid=True), ForeignKey(Events.id), nullable=True)
    swarm_health_status_id = Column(
        UUID(as_uuid=True), ForeignKey(SwarmHealthStatuses.id), nullable=True
    )
    hive_condition_id = Column(
        UUID(as_uuid=True), ForeignKey(HiveConditions.id), nullable=True
    )

    created_at = Column(TIMESTAMP(), default=datetime.datetime.utcnow)
    updated_at = Column(
        TIMESTAMP(), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )
    deleted_at = Column(TIMESTAMP(), nullable=True)

    user = relationship(Users, backref="comments")
    type = relationship(CommentTypes)
    swarm_health_status = relationship(SwarmHealthStatuses)
    hive_condition = relationship(HiveConditions)
    swarm = relationship(Swarms, backref="comments")
    hive = relationship(Hives, backref="comments")
    apiary = relationship(Apiaries, backref="comments")
    event = relationship(Events, backref=backref("comment", uselist=False))
