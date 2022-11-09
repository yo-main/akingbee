from dataclasses import dataclass
from uuid import UUID

from akb.domains.bee.entities.vo.reference import Reference


@dataclass(slots=True)
class UserEntity:
    public_id: Reference

    def __eq__(self, other):
        return self.public_id == other.public_id
