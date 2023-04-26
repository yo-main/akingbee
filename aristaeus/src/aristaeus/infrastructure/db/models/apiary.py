from uuid import UUID

from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy import text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import column_property

from aristaeus.domain.entities.apiary import ApiaryEntity

from .base import BaseModel
from .hive import HiveModel


class ApiaryModel(BaseModel):
    id: Mapped[int] = mapped_column(primary_key=True)
    public_id: Mapped[UUID] = mapped_column(unique=True)
    name: Mapped[str]
    location: Mapped[str]
    honey_kind: Mapped[str]
    organization_id: Mapped[UUID]

    hive_count: Mapped[int] = column_property(
        select(func.count(HiveModel.id))
        .where(HiveModel.apiary_id == id)
        .correlate_except(HiveModel)
        .scalar_subquery()
    )

    hives: Mapped[list["HiveModel"]] = relationship(back_populates="apiary")

    def to_entity(self) -> ApiaryEntity:
        return ApiaryEntity(
            public_id=self.public_id,
            name=self.name,
            location=self.location,
            honey_kind=self.honey_kind,
            organization_id=self.organization_id,
            hive_count=self.hive_count,
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
