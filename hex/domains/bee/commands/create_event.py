from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class CreateEventCommand:
    hive: UUID
    due_date: datetime
    type: str
    status: str
    title: str
    description: str
