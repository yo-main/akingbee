from uuid import UUID

from akingbee.domains.aristaeus.entities.apiary import ApiaryEntity
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class ApiaryModel(BaseModel):
    public_id: Mapped[UUID]
    name: Mapped[str]
    location: Mapped[str]
    honey_kind: Mapped[str]
    organization_id: Mapped[UUID]

    def to_entity(self) -> ApiaryEntity:
        return ApiaryEntity(
            public_id=self.public_id,
            name=self.name,
            location=self.location,
            honey_kind=self.honey_kind,
            organization_id=self.organization_id,
        )

    @staticmethod
    def from_entity(entity: ApiaryEntity) -> "ApiaryModel":
        return ApiaryModel(
            public_id=entity.public_id,
            name=entity.name,
            location=entity.location,
            honey_kind=entity.honey_kind,
            organization_id=entity.organization_id,
        )
