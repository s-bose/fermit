"""
Primitives for actions.

Actions are what an actor is attempting to perform
on a resource.
Commonly used actions are CRUD (Create, Read, Update, Delete).

Actions, after created are immutable.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Self, final

if TYPE_CHECKING:
    from fermit.core.resource import Resource


@final
class Action:
    __slots__ = ("_name", "_description", "_alias")

    def __init__(
        self,
        name: str,
        *,
        description: str | None = None,
        aliases: tuple[str, ...] | None = None,
    ) -> None:
        if not name.isidentifier():
            raise ValueError(f"Action name must be a valid identifier, got {name}")

        self._name = name
        self._description = description
        self._aliases = aliases

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str | None:
        return self._description

    @property
    def aliases(self) -> tuple[str, ...]:
        return self._aliases or ()


@final
class BoundAction:
    def __init__(
        self,
        resource: type[Resource],
        name: str,
        position: int,
        description: str | None = None,
        aliases: tuple[str, ...] | None = None,
    ):
        self._resource = resource
        self._name = name
        self._description = description
        self._aliases = aliases
        self._position = position
        self._mask = 1 << position

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str | None:
        return self._description

    @property
    def alias(self) -> tuple[str, ...]:
        return self._aliases or ()

    def __repr__(self):
        return f"{self._resource}.{self._name}: {self._position}"
