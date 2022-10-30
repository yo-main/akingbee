from uuid import UUID

from domains.bee.entities.hive import HiveEntity
from domains.bee.entities.vo.reference import Reference
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel
from .apiary import ApiaryModel


class HiveModel(BaseModel):
    public_id: Mapped[UUID]
    name: Mapped[str]
    condition: Mapped[str]
    owner: Mapped[str]
    apiary: Mapped[ApiaryModel]

    def to_entity(self) -> HiveEntity:
        return HiveEntity(
            public_id=Reference.of(self.public_id),
            name=self.name,
            condition=self.condition,
            owner=self.owner,
            apiary=self.apiary.to_entity(),
        )

    @staticmethod
    def from_entity(entity: HiveEntity) -> "HiveModel":
        return HiveModel(
            public_id=entity.public_id.get(),
            name=entity.name,
            condition=entity.condition,
            owner=entity.owner,
            apiary=ApiaryModel.from_entity(entity.apiary),
        )
