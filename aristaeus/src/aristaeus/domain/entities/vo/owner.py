from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Owner:
    value: str
