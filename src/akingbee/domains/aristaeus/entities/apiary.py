import uuid
from dataclasses import dataclass

from domains.bee.entities.vo.reference import Reference


@dataclass(slots=True)
class ApiaryEntity:
    public_id: Reference
    name: str
    location: str
    honey_kind: str

    @staticmethod
    def create(name: str, location: str, honey_kind: str) -> "ApiaryEntity":
        return ApiaryEntity(
            public_id=Reference.of(uuid.uuid4()),
            name=name,
            location=location,
            honey_kind=honey_kind,
        )
