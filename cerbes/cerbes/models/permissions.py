import datetime
import uuid

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import BOOLEAN, TIMESTAMP, UUID
from sqlalchemy.orm import backref, relationship

from .base import Base
from .users import Users


class Permissions(Base):
    __tablename__ = "permissions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey(Users.id), nullable=False, index=True
    )

    impersonate = Column(BOOLEAN(), default=False, nullable=False)

    created_at = Column(TIMESTAMP(), default=datetime.datetime.utcnow)
    updated_at = Column(
        TIMESTAMP(), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )
    deleted_at = Column(TIMESTAMP(), nullable=True)

    user = relationship(Users, backref=backref("permissions", uselist=False))
