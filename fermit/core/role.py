from typing import ClassVar
from abc import ABC

from fermit.core.action import BoundAction, ActionSet


class Role(ABC):
    name: ClassVar[str | None] = None
    description: ClassVar[str | None] = None

    permissions: list[BoundAction | ActionSet]

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        if cls.name is None:
            cls.name = cls.__name__

        if not cls.permissions:
            raise TypeError(f"Role {cls.name} must have permissions defined")
