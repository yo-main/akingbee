import uuid
from dataclasses import dataclass

from domains.bee.entities.vo.reference import Reference

from .apiary import ApiaryEntity


@dataclass(slots=True)
class HiveEntity:
    public_id: Reference
    name: str
    condition: str
    owner: str
    apiary: ApiaryEntity

    @staticmethod
    def create(name: str, owner: str, condition: str, apiary: ApiaryEntity) -> "HiveEntity":
        return HiveEntity(
            public_id=Reference.of(uuid.uuid4()),
            name=name,
            owner=owner,
            condition=condition,
            apiary=apiary,
        )
