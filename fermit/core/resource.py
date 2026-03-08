from __future__ import annotations

from typing import Any, ClassVar, Mapping

from fermit.core.action import BoundAction
from fermit.core.constants import MAX_ACTIONS_PER_RESOURCE
from fermit.core.relation import BoundRelation


class ResourceMeta(type):

    def __call__(cls, *args, **kwargs):
        if cls.__name__ == "Resource":
            raise TypeError("Resource base class is not instantiable")

        if len(args) == 1 and isinstance(args[0], str) and not kwargs:
            name = args[0]
            if name in cls.__dict__:
                return cls.__dict__[name]
            if name in cls.__aliases__:
                return cls.__aliases__[name]
            raise AttributeError(f"{cls.__name__} has no action '{name}'")

        raise TypeError(f"Resource {cls.__name__} is not instantiable")

    def __getattr__(cls, name: str) -> Any:
        if name in cls.__dict__:
            return cls.__dict__[name]
        if name in cls.__aliases__:
            return cls.__aliases__[name]
        raise AttributeError(f"{cls.__name__} has no action '{name}'")


class Resource(metaclass=ResourceMeta):
    """Base class that can be subclassed to make new Resource classes

    A Resource subclass is immutable and frozen and
    cannot be instantiated

    Actions for a resource can be defined as class attributes and
    initialised with calling `Action()` helper which will return a
    `BoundAction` instance

    The position of the action will be determined by the order of definition
    in the class body, starting from 0

    """

    __resource_name__: ClassVar[str | None] = None
    __bound_actions__: ClassVar[Mapping[str, BoundAction]]
    __relationships__: ClassVar[Mapping[str, BoundRelation]]
    __aliases__: ClassVar[Mapping[str, BoundAction]]

    def __init_subclass__(cls) -> None:
        for base in cls.__bases__:
            if isinstance(base, ResourceMeta) and base.__name__ != "Resource":
                raise TypeError(
                    f"Resource {cls.__name__} cannot inherit from another Resource {base.__name__}"
                )

        aliases: dict[str, BoundAction] = {}
        bound_actions: dict[str, BoundAction] = {}

        filtered_actions = {
            key: value
            for key, value in cls.__dict__.items()
            if isinstance(value, BoundAction)
        }

        filtered_relations = {
            key: value
            for key, value in cls.__dict__.items()
            if isinstance(value, BoundRelation)
        }

        cls.__relationships__ = cls.initialize_relationships(filtered_relations)

        for index, (key, value) in enumerate(filtered_actions.items()):

            if index >= MAX_ACTIONS_PER_RESOURCE:
                raise ValueError(
                    f"Action {key} does not have a position and "
                    f"the index {index} exceeds the maximum allowed"
                    " actions per resource"
                )

            value = BoundAction(
                name=key,
                resource=cls,
                position=index,
                description=value.description,
                aliases=value.aliases,
                serialize_as=value.serialize_as,
            )

            bound_actions[key] = value
            setattr(cls, key, value)

            if value.aliases is not None:
                for alias in value.aliases:
                    if alias in aliases:
                        raise ValueError(
                            f"Action {key} has an alias {alias} that conflicts with another action"
                        )
                    aliases[alias] = value

        cls.__bound_actions__ = bound_actions
        cls.__aliases__ = aliases

    @classmethod
    def mask(cls, include: list[BoundAction] | str | None = None):
        mask = 0

        if isinstance(include, str) and include == "*" or include is None:
            for value in cls.__bound_actions__.values():
                mask |= value.mask()
            return mask

        if isinstance(include, list):
            for action in include:
                if action.resource is not cls:
                    raise ValueError(
                        f"Action {action.name} does not belong to resource {cls.__name__}"
                    )
                mask |= action.mask()
            return mask

        return mask

    def __new__(cls, *args, **kwargs): ...  # to satisfy type checker

    @classmethod
    def initialize_relationships(
        cls, relations: dict[str, BoundRelation]
    ) -> dict[str, BoundRelation]:
        relationship_map: dict[str, BoundRelation] = {}
        for relation_var_name, relation in relations.items():
            relation_key = relation.name if relation.name else relation_var_name
            bound_relation = BoundRelation(
                target=relation.target,
                name=relation_key,
                owner=relation.owner if relation.owner else cls,
                description=relation.description,
            )

            relationship_map[relation_key] = bound_relation
            setattr(cls, relation_key, bound_relation)

        return relationship_map

    @classmethod
    def actions(cls) -> frozenset[BoundAction]:
        return frozenset(cls.__bound_actions__.values())
