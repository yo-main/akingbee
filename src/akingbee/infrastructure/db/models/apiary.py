from uuid import UUID

from domains.bee.entities.apiary import ApiaryEntity
from domains.bee.entities.vo.reference import Reference
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class ApiaryModel(BaseModel):
    public_id: Mapped[UUID]
    name: Mapped[str]
    location: Mapped[str]
    honey_kind: Mapped[str]

    def to_entity(self) -> ApiaryEntity:
        return ApiaryEntity(
            public_id=Reference.of(self.public_id),
            name=self.name,
            location=self.location,
            honey_kind=self.honey_kind,
        )

    @staticmethod
    def from_entity(entity: ApiaryEntity) -> "ApiaryModel":
        return ApiaryModel(
            public_id=entity.public_id.get(),
            name=entity.name,
            location=entity.location,
            honey_kind=entity.honey_kind,
        )
