from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship

from aristaeus.domain.entities.apiary import ApiaryEntity

from .base import BaseModel


class ApiaryModel(BaseModel):
    public_id: Mapped[UUID] = mapped_column(unique=True)
    name: Mapped[str]
    location: Mapped[str]
    honey_kind: Mapped[str]
    organization_id: Mapped[UUID]

    hives: Mapped[list["HiveModel"]] = relationship(back_populates="apiary")

    def to_entity(self) -> ApiaryEntity:
        return ApiaryEntity(
            public_id=self.public_id,
            name=self.name,
            location=self.location,
            honey_kind=self.honey_kind,
            organization_id=self.organization_id,
            hive_count=len(self.hives)
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
