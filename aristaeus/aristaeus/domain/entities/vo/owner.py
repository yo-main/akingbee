from dataclasses import dataclass


@dataclass(frozen=True)
class Owner:
    value: str
