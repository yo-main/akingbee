from dataclasses import asdict
from typing import Protocol


class Entity(Protocol):
    def asdict(self) -> dict:
        return asdict(self)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return TypeError(f"Cannot compare {self} with {other}")
        return self.public_id == other.public_id
