from uuid import UUID

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from aristaeus.domain.entities.parameter import ParameterEntity

from .base import BaseModel


class ParameterModel(BaseModel):
    public_id: Mapped[UUID] = mapped_column(unique=True)
    key: Mapped[str]
    value: Mapped[str]
    organization_id: Mapped[UUID]

    __table_args__ = (UniqueConstraint("key", "value", "organization_id"),)

    def to_entity(self) -> ParameterEntity:
        return ParameterEntity(
            key=self.key, value=self.value, organization_id=self.organization_id, public_id=self.public_id
        )

    @staticmethod
    def from_entity(entity: ParameterEntity) -> "ParameterModel":
        return ParameterModel(
            key=entity.key,
            value=entity.value,
            public_id=entity.public_id,
            organization_id=entity.organization_id,
        )
