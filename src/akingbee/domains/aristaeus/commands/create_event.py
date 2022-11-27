from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class CreateEventCommand:
    hive_id: UUID
    due_date: datetime
    type: str
    status: str
    title: str
    description: str
