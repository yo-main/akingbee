import datetime
import uuid

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import TIMESTAMP, TEXT, BYTEA, UUID

from .base import Base


class Users(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(TEXT(), unique=True, nullable=False)

    created_at = Column(TIMESTAMP(), default=datetime.datetime.utcnow)
    updated_at = Column(TIMESTAMP(), default=datetime.datetime.now, onupdate=datetime.datetime.now)

class Credentials(Base):
    __tablename__ = "credentials"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey(Users.id), nullable=False)
    username = Column(TEXT(), unique=True, nullable=False)
    password = Column(BYTEA(), nullable=False)
    last_seen = Column(TIMESTAMP())

    created_at = Column(TIMESTAMP(), default=datetime.datetime.now)
    updated_at = Column(TIMESTAMP(), default=datetime.datetime.now, onupdate=datetime.datetime.now)

    user = relationship(Users, backref="credentials", uselist=False)

class Owners(Base):
    __tablename__ = "owners"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey(Users.id), nullable=False)
    surname = Column(TEXT(), nullable=False)

    created_at = Column(TIMESTAMP(), default=datetime.datetime.now)
    updated_at = Column(TIMESTAMP(), default=datetime.datetime.now, onupdate=datetime.datetime.now)

    user = relationship(Users, backref="owners")

