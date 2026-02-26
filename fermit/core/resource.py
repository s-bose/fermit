from __future__ import annotations

from typing import ClassVar, Mapping

from fermit.core.action import BoundAction, ActionSet
from fermit.core.constants import MAX_ACTIONS_PER_RESOURCE


class Resource:
    _bound_actions: ClassVar[Mapping[str, BoundAction]]

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        for base in cls.__bases__:
            if base is not Resource and issubclass(base, Resource):
                raise TypeError(
                    f"Resource {cls.__name__} cannot inherit from another resource {base.__name__}"
                )

        filtered_fields = {
            k: v for k, v in cls.__dict__.items() if isinstance(v, BoundAction)
        }
        if len(filtered_fields) > MAX_ACTIONS_PER_RESOURCE:
            raise ValueError(
                f"Resource {cls.__name__} cannot have more than {MAX_ACTIONS_PER_RESOURCE} actions"
            )

        for index, (key, value) in enumerate(filtered_fields.items()):
            if value.position and value.position != index:
                raise ValueError(
                    f"Action {key} has a position that is not the expected index {index}"
                )
            bound_action = BoundAction(
                name=key,
                resource=cls,
                position=index,
                description=value.description,
                aliases=value.aliases,
                serialize_as=value.serialize_as,
            )
            filtered_fields[key] = bound_action

        cls._bound_actions = filtered_fields
        for key, bound_action in filtered_fields.items():
            setattr(cls, key, bound_action)

    def __new__(cls, *args, **kwargs):
        if cls is not Resource:
            raise TypeError(f"Resource {cls.__name__} is not instantiable")
        return super().__new__(cls, *args, **kwargs)

    @property
    def all(self) -> ActionSet:
        values = self._bound_actions.values()
        return ActionSet.from_actions(
            *values, description="All actions for this resource"
        )
