import uuid
from dataclasses import dataclass
from domains.bee.entities.vo.reference import Reference

@dataclass(slots=True)
class SettingEntity:
    public_id: Reference
    key: str
    value: str
    
    @staticmethod
    def create(key: str, value: str) -> "SettingEntity":
        return SettingEntity(
            public_id=Reference.of(uuid.uuid4()),
            key=key,
            value=value,
        )
