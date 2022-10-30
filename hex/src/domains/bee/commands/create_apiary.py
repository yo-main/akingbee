from dataclasses import dataclass
from uuid import UUID


@dataclass
class CreateApiaryCommand:
    name: str
    location: str
    honey_kind: str
