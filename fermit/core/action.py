"""
Primitives for actions.

Actions are what an actor is attempting to perform
on a resource.
Commonly used actions are CRUD (Create, Read, Delete).

Actions, after created are immutable.
"""

from __future__ import annotations

from asyncio import Runner
from dataclasses import dataclass
from typing import TYPE_CHECKING, overload

if TYPE_CHECKING:
    from fermit.core.resource import Resource


@overload
def Action(
    name: str,
    *,
    description: str | None = ...,
    aliases: tuple[str, ...] | None = ...,
    serialize_as: str | None = ...,
) -> BoundAction: ...
@overload
def Action(
    *,
    description: str | None = ...,
    aliases: tuple[str, ...] | None = ...,
    serialize_as: str | None = ...,
) -> BoundAction: ...


def Action(
    name: str | None = None,
    *,
    description: str | None = None,
    aliases: tuple[str, ...] | None = None,
    serialize_as: str | None = None,
) -> BoundAction:
    return BoundAction(name=name, description=description, aliases=aliases, serialize_as=serialize_as)


@dataclass(frozen=True, slots=True)
class BoundAction:
    name: str | None = None
    position: int | None = None
    description: str | None = None
    aliases: tuple[str, ...] | None = None
    resource: type[Resource] | None = None
    serialize_as: str | None = None

    def __repr__(self) -> str:
        if not self.resource:
            raise RuntimeError("no resource configured, invalid action")
        return f"{self.resource.__name__}.{self.name} #{self.position}"

    @property
    def value(self) -> str:
        if self.serialize_as:
            return self.serialize_as
        return self.__repr__()

    def __eq__(self, other: object, /) -> bool:
        if not isinstance(other, BoundAction):
            raise NotImplementedError()

        return other.resource is self.resource and other.name == self.name and other.position == self.position

    def __hash__(self) -> int:
        return hash((id(self.resource), self.name, self.position))

    def mask(self):
        if not self.position:
            raise RuntimeError("position is not set, cannot mask")

        return 1 << self.position
