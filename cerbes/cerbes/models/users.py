import datetime
import uuid

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import BOOLEAN, TEXT, TIMESTAMP, UUID

from .base import Base


class Users(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(TEXT(), unique=True, nullable=False)
    activation_id = Column(UUID(as_uuid=True), nullable=True, default=uuid.uuid4)
    activated = Column(BOOLEAN(), nullable=False, default=False)

    created_at = Column(TIMESTAMP(), default=datetime.datetime.utcnow)
    updated_at = Column(
        TIMESTAMP(), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )
    deleted_at = Column(TIMESTAMP(), nullable=True)
