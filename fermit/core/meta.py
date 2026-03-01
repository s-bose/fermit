from __future__ import annotations
from enum import _EnumDict, EnumType
from typing import Any, ClassVar, Mapping

from fermit.core.action import BoundAction


class BaseEnumMeta(EnumType):
    def __new__(
        metacls,
        name: str,
        bases: tuple[type, ...],
        namespace: _EnumDict,
        **kwds: Any,
    ):
        cls = super().__new__(metacls, name, bases, namespace, **kwds)

        cls._member_names_ = []
        cls._member_map_ = {}
        cls._value2member_map_ = {}

        # filtered_fields = v for k, v in cls if isinstance(v, BoundAction)}

        # if not filtered_fields:
        #     return cls
