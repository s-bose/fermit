from abc import ABC
from typing import ClassVar

from fermit.core import ActionSet
from fermit.core.action import BoundAction


class Role(ABC):
    name: ClassVar[str | None] = None
    description: ClassVar[str | None] = None

    permissions: list[BoundAction | ActionSet]

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        if cls.name is None:
            cls.name = cls.__name__

        if not cls.permissions:
            return

        permissions_set = set(cls.permissions)

        for base in cls.__bases__:
            if issubclass(base, Role) and base.__name__ != "Role":
                permissions_set.update(base.permissions)
