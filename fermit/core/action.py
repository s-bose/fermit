"""
Primitives for actions.

Actions are what an actor is attempting to perform
on a resource.
Commonly used actions are CRUD (Create, Read, Update, Delete).

Actions, after created are immutable.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fermit.core.resource import Resource


@dataclass(frozen=True, slots=True)
class Action:
    name: str
    description: str | None = None
    aliases: tuple[str, ...] | None = None


@dataclass(frozen=True, slots=True)
class BoundAction:
    resource: type[Resource]
    name: str
    position: int
    description: str | None = None
    aliases: tuple[str, ...] | None = None

    def __repr__(self):
        return f"{self.resource}.{self.name}: {self.position}"

    @classmethod
    def from_action(cls, action: Action, resource: type[Resource], position: int):
        return cls(
            resource=resource,
            name=action.name,
            position=position,
            description=action.description,
            aliases=action.aliases,
        )
