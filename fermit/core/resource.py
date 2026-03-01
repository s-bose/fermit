from __future__ import annotations

from typing import ClassVar, Mapping

from fermit.core.action import BoundAction
from fermit.core.constants import MAX_ACTIONS_PER_RESOURCE


class Resource:
    mask: ClassVar[int] = 0
    implies: dict[BoundAction, list[BoundAction]]

    _bound_actions: ClassVar[Mapping[str, BoundAction]]

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        merged_actions: dict[str, BoundAction] = {}
        for base in cls.__bases__:
            if issubclass(base, Resource) and base is not Resource:
                # inherit all bound actions from parent resource classes
                if not hasattr(base, "_bound_actions"):
                    continue
                for key, value in base._bound_actions.items():
                    merged_actions[key] = value

        filtered_fields = {
            k: v for k, v in cls.__dict__.items() if isinstance(v, BoundAction)
        }

        if not filtered_fields:
            return

        if len(filtered_fields) > MAX_ACTIONS_PER_RESOURCE:
            raise ValueError(
                f"Resource {cls.__name__} cannot have more than {MAX_ACTIONS_PER_RESOURCE} actions"
            )

        merged_actions.update(filtered_fields)

        for index, (key, value) in enumerate(merged_actions.items()):
            if value.position and value.position != index:
                raise ValueError(
                    f"Action {key} has a position that is not the expected index {index}"
                )
            if value.position is None:
                if index >= MAX_ACTIONS_PER_RESOURCE:
                    raise ValueError(
                        f"Action {key} does not have a position and the index {index} exceeds the maximum allowed actions per resource"
                    )

                value = BoundAction(
                    name=key,
                    resource=cls,
                    position=index,
                    description=value.description,
                    aliases=value.aliases,
                    serialize_as=value.serialize_as,
                )
            merged_actions[key] = value
            cls.mask |= value.mask()
            if cls.mask >= 1 << MAX_ACTIONS_PER_RESOURCE:
                raise ValueError(
                    f"Action {cls.__name__}.{key} exceedsthe maximum allowed actions per resource"
                )

        cls._bound_actions = merged_actions
        for key, bound_action in merged_actions.items():
            setattr(cls, key, bound_action)

    def __new__(cls, *args, **kwargs):
        if cls is not Resource:
            raise TypeError(f"Resource {cls.__name__} is not instantiable")
        return super().__new__(cls, *args, **kwargs)
