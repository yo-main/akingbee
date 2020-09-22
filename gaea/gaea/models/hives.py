import datetime
import uuid

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import TIMESTAMP, TEXT, BYTEA, UUID

from .base import Base
from .users import Users, Owners
from .apiaries import Apiaries
from .swarms import Swarms


class HiveConditions(Base):
    __tablename__ = "hive_conditions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(TEXT(), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey(Users.id), nullable=False)

    created_at = Column(TIMESTAMP(), default=datetime.datetime.utcnow)
    updated_at = Column(
        TIMESTAMP(), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )
    deleted_at = Column(TIMESTAMP(), nullable=True)

    user = relationship(Users, backref="hive_conditions")


class Hives(Base):
    __tablename__ = "hives"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(TEXT(), nullable=False)

    user_id = Column(UUID(as_uuid=True), ForeignKey(Users.id), nullable=False)
    condition_id = Column(
        UUID(as_uuid=True), ForeignKey(HiveConditions.id), nullable=False
    )
    owner_id = Column(UUID(as_uuid=True), ForeignKey(Owners.id), nullable=True)
    swarm_id = Column(UUID(as_uuid=True), ForeignKey(Swarms.id), nullable=True)
    apiary_id = Column(UUID(as_uuid=True), ForeignKey(Apiaries.id), nullable=True)

    created_at = Column(TIMESTAMP(), default=datetime.datetime.utcnow)
    updated_at = Column(
        TIMESTAMP(), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )
    deleted_at = Column(TIMESTAMP(), nullable=True)

    user = relationship(Users, backref="hives")
    owner = relationship(Owners, backref="hives")
    swarm = relationship(Swarms, backref=backref("hive", uselist=False))
    apiary = relationship(Apiaries, backref="hives")
    condition = relationship(HiveConditions, backref="hives")
