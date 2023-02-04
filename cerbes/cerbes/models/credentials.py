import datetime
import uuid

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import BYTEA, TEXT, TIMESTAMP, UUID
from sqlalchemy.orm import relationship

from .base import Base
from .users import Users


class Credentials(Base):
    __tablename__ = "credentials"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(TEXT(), unique=True, nullable=False)
    password = Column(BYTEA(), nullable=False)
    last_seen = Column(TIMESTAMP())
    user_id = Column(UUID(as_uuid=True), ForeignKey(Users.id), nullable=False)
    reset_id = Column(UUID(as_uuid=True), nullable=True)

    created_at = Column(TIMESTAMP(), default=datetime.datetime.utcnow)
    updated_at = Column(
        TIMESTAMP(), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )

    user = relationship(Users, backref="credentials", uselist=False)
