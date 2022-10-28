from typing import Protocol

from domains.bee.entities.user import UserEntity
from domains.bee.entities.vo.reference import Reference


class UserRepositoryAdapter(Protocol):
    def create(self, user: UserEntity) -> None:
        ...

    def get(self, reference: Reference) -> UserEntity:
        ...
