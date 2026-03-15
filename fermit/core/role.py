from dataclasses import dataclass
from typing import Any, ClassVar

from fermit.core import ActionSet, Resource
from fermit.core.action import BoundAction


@dataclass(slots=True)
class RoleInstance:
    name: str | None
    permissions: list[BoundAction]


class Role:
    name: ClassVar[str | None] = None
    description: ClassVar[str | None] = None

    permissions: ClassVar[list[BoundAction | ActionSet]]
    scopes: ClassVar[str | list[type[Resource]] | None] = None

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if cls.name is None:
            cls.name = cls.__name__

        if not cls.permissions:
            return

        permissions_set = set(cls.permissions)

        for base in cls.__bases__:
            if issubclass(base, Role) and base.__name__ != "Role":
                permissions_set.update(base.permissions)

        cls.permissions = list(permissions_set)

        _scopes: set[type[Resource]] = set()
        _permission_scopes = set(p.resource for p in cls.permissions if p.resource)
        if not cls.scopes:
            return

        declared_scopes = cls.scopes
        if isinstance(declared_scopes, list):
            _scopes.update(declared_scopes)

        if cls.scopes == "*":
            # Wildcard: derive scopes from all permission resources
            _scopes.update(_permission_scopes)

        if _permission_scopes and not _scopes.issubset(_permission_scopes):
            raise ValueError(
                f"Invalid scopes for role '{cls.name}': {cls.scopes}. "
                f"All scopes must be derived from permissions: {_permission_scopes}"
            )

        for permission in cls.permissions:
            if not permission.resource or permission.resource not in _scopes:
                continue

        cls.scopes = list(_scopes)

    @classmethod
    def get_scopes(cls) -> frozenset[type[Resource]]:
        scopes = frozenset[type[Resource]]()
        if isinstance(cls.scopes, str):
            raise ValueError(
                f"Error with class initialization, wildcard scopes should "
                f"have been resolved to actual resource classes: {cls.scopes}"
            )

        if not cls.scopes:
            return scopes

        return frozenset(cls.scopes)

    def __new__(cls, name: str | None = None, *, permissions: list[BoundAction]) -> RoleInstance:
        return RoleInstance(name=name, permissions=permissions)
