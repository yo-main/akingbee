from uuid import UUID

from akingbee.domains.aristaeus.entities.hive import HiveEntity
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel
from .apiary import ApiaryModel


class HiveModel(BaseModel):
    public_id: Mapped[UUID]
    name: Mapped[str]
    condition: Mapped[str]
    owner_id: Mapped[UUID]
    organization_id: Mapped[UUID]
    apiary_id: Mapped[UUID | None]

    def to_entity(self) -> HiveEntity:
        return HiveEntity(
            public_id=self.public_id,
            name=self.name,
            condition=self.condition,
            owner_id=self.owner_id,
            organization_id=self.organization_id,
            apiary_id=self.apiary_id,
        )

    @staticmethod
    def from_entity(entity: HiveEntity) -> "HiveModel":
        return HiveModel(
            public_id=entity.public_id,
            name=entity.name,
            condition=entity.condition,
            owner_id=entity.owner_id,
            organization_id=entity.organization_id,
            apiary_id=entity.apiary_id,
        )
