from typing import Protocol


class Entity(Protocol):
    def asdict(self) -> dict:
        ...
