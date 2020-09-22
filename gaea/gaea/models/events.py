import datetime
import uuid

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import TIMESTAMP, TEXT, BYTEA, UUID

from .base import Base
from .users import Users
from .apiaries import Apiaries
from .hives import Hives


class EventTypes(Base):
    __tablename__ = "event_types"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(TEXT(), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey(Users.id), nullable=False)

    created_at = Column(TIMESTAMP(), default=datetime.datetime.utcnow)
    updated_at = Column(
        TIMESTAMP(), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )
    deleted_at = Column(TIMESTAMP(), nullable=True)

    user = relationship(Users, backref="event_types")


class EventStatuses(Base):
    __tablename__ = "event_statuses"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(TEXT(), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey(Users.id), nullable=False)

    created_at = Column(TIMESTAMP(), default=datetime.datetime.utcnow)
    updated_at = Column(
        TIMESTAMP(), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )
    deleted_at = Column(TIMESTAMP(), nullable=True)

    user = relationship(Users, backref="event_statuses")


class Events(Base):
    __tablename__ = "events"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(TEXT(), nullable=False)
    description = Column(TEXT(), nullable=True)
    due_date = Column(TIMESTAMP(), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey(Users.id), nullable=False)
    type_id = Column(UUID(as_uuid=True), ForeignKey(EventTypes.id), nullable=False)
    status_id = Column(UUID(as_uuid=True), ForeignKey(EventStatuses.id), nullable=False)
    hive_id = Column(UUID(as_uuid=True), ForeignKey(Hives.id), nullable=True)
    apiary_id = Column(UUID(as_uuid=True), ForeignKey(Apiaries.id), nullable=True)

    created_at = Column(TIMESTAMP(), default=datetime.datetime.utcnow)
    updated_at = Column(
        TIMESTAMP(), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )
    deleted_at = Column(TIMESTAMP(), nullable=True)

    user = relationship(Users, backref="events")
    type = relationship(EventTypes)
    status = relationship(EventStatuses)
    hive = relationship(Hives, backref="events")
    apiary = relationship(Apiaries, backref="events")
