from dataclasses import dataclass
from uuid import UUID


@dataclass
class CreateHiveCommand:
    condition: str
    apiary: UUID
    owner: str
    name: str
