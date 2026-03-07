from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fermit.core.resource import Resource


def Relation(
    target: type[Resource],
    *,
    description: str | None = None,
    name: str | None = None,
):
    return BoundRelation(target=target, name=name, description=description)


@dataclass(frozen=True, slots=True)
class BoundRelation:
    target: type[Resource]
    name: str | None = None
    owner: type[Resource] | None = None
    description: str | None = None
