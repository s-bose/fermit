"""
Primitives for actions.

Actions are what an actor is attempting to perform
on a resource.
Commonly used actions are CRUD (Create, Read, Delete).

Actions, after created are immutable.
"""

from __future__ import annotations

from typing import Callable, TYPE_CHECKING, overload
from functools import lru_cache

from dataclasses import dataclass

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
    """
    Helper function to create a `BoundAction` instance

    Args:
        name (str | None, optional): The name of the action
        description (str | None, optional): A description of the action
        aliases (tuple[str, ...] | None, optional): Alternative names for the action
        serialize_as (str | None, optional): The name to use when serializing the action

    Returns:
        BoundAction
    """

    return BoundAction(
        name=name,
        description=description,
        aliases=aliases,
        serialize_as=serialize_as,
    )


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

        name = self.serialize_as if self.serialize_as is not None else self.name
        if not name:
            raise RuntimeError("no name configured, invalid action")
        return f"{self.resource.__name__}.{name} #{self.position}"

    def __or__(self, other: object, /):
        pass

    @property
    def value(self) -> str:
        return str(self.mask())

    def mask(self):
        if self.position is None:
            raise RuntimeError("position is not set, cannot mask")

        return 1 << self.position

    def __eq__(self, other: object, /) -> bool:
        if not isinstance(other, BoundAction):
            raise NotImplementedError()

        return (
            other.resource is self.resource
            and other.name == self.name
            and other.position == self.position
        )

    def __hash__(self) -> int:
        return hash((id(self.resource), self.name, self.position))


@dataclass(frozen=True, slots=True)
class ActionSet:
    resource: type[Resource]
    actions: list[BoundAction]
    description: str | None = None

    def mask(self):
        mask = 0
        for action in self.actions:
            mask |= action.mask()
        return mask

    @classmethod
    def from_actions(cls, *actions: BoundAction, description: str | None = None):
        resources = {a.resource for a in actions if a.resource is not None}
        if not resources or len(resources) > 1:
            raise ValueError("all actions must belong to the same resource")

        return cls(
            resource=list(resources)[0], actions=list(actions), description=description
        )
