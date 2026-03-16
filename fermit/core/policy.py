from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Policy:
    name: str
    description: str | None = None
