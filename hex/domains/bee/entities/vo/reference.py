from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True)
class Reference:
    value: UUID

    @staticmethod
    def of(value: UUID) -> "Reference":
        return Reference(value=value)

    def get(self) -> UUID:
        return self.value

    def __str__(self):
        return str(self.value)
