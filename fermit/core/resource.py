from __future__ import annotations

from typing import Any

from fermit.core.action import Action, BoundAction
from fermit.core.constants import MAX_ACTIONS_PER_RESOURCE


class Resource:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        for base in cls.__bases__:
            if base is not Resource and issubclass(base, Resource):
                raise TypeError(
                    f"Resource {cls.__name__} cannot inherit from another resource {base.__name__}"
                )

        actions: tuple[Any, ...] = namespace.get("actions", ())
        if not actions:
            raise ValueError(f"Resource {name} must define at least one action")

        if len(actions) > MAX_ACTIONS_PER_RESOURCE:
            raise ValueError(f"Resource {name} cannot have more than {MAX_ACTIONS_PER_RESOURCE} actions")

        filtered_actions: list[Action] = []
        unique_action_names = set[str]()
        for entry in actions:
            if isinstance(entry, str):
                entry = Action(
                    name=entry,
                )
            elif not isinstance(entry, Action):
                raise TypeError(f"Entries in 'actions' must be a str or Action, got {type(entry).__name__}")

            if entry.name in unique_action_names:
                raise ValueError(f"Action {entry.name} already exists in resource")

            if len(entry.name.split(".")) > 1:
                raise ValueError(f"Action name {entry.name} cannot contain dots")

            unique_action_names.add(entry.name)
            filtered_actions.append(entry)
