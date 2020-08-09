import datetime
import uuid

from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import DATETIME, VARCHAR

from .base import Base, UUID


class Users(Base):
    __tablename__ = "users"
    id = Column(UUID(), primary_key=True, unique=True, default=uuid.uuid4)
    username = Column(VARCHAR(256), unique=True)
    pwd = Column(VARCHAR(256))
    email = Column(VARCHAR(256), unique=True)
    created_at = Column(DATETIME, default=datetime.datetime.utcnow)
    updated_at = Column(DATETIME, default=datetime.datetime.utcnow)


class Owners(Base):
    __tablename__ = "owners"
    id = Column(UUID(), primary_key=True, unique=True, default=uuid.uuid4)
    name = Column(VARCHAR(256))
    user = relationship(Users, back_populates="owners")
    date_creation = Column(DATETIME, default=datetime.datetime.now)
    date_modification = Column(DATETIME, default=datetime.datetime.now)
