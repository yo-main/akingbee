from uuid import UUID

from akingbee.domains.aristaeus.entities.user import UserEntity
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class UserModel(BaseModel):
    public_id: Mapped[UUID]
    organization_id: Mapped[UUID]

    def to_entity(self) -> UserEntity:
        return UserEntity(public_id=self.public_id, organization_id=self.organization_id)

    @staticmethod
    def from_entity(entity: UserEntity) -> "UserModel":
        return UserModel(
            public_id=entity.public_id,
            organization_id=entity.organization_id,
        )
