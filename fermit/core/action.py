"""
Primitives for actions.

Actions are what an actor is attempting to perform
on a resource.
Commonly used actions are CRUD (Create, Read, Update, Delete).

Actions, after created are immutable.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar, overload

if TYPE_CHECKING:
    from fermit.core.resource import Resource


@overload
def Action(
    name: str,
    *,
    description: str | None = ...,
    aliases: tuple[str, ...] | None = ...,
) -> BoundAction: ...
@overload
def Action(
    *,
    description: str | None = ...,
    aliases: tuple[str, ...] | None = ...,
) -> BoundAction: ...


def Action(
    name: str | None = None,
    *,
    description: str | None = None,
    aliases: tuple[str, ...] | None = None,
) -> BoundAction:
    return BoundAction(
        name=name,
        description=description,
        aliases=aliases,
    )


@dataclass(frozen=True, slots=True)
class BoundAction:
    name: str | None = None
    position: int | None = None
    description: str | None = None
    aliases: tuple[str, ...] | None = None
    resource: type[Resource] | None = None
