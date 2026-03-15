from typing import Any, Protocol

from fermit.core.action import BoundAction


class PolicyEnforcer(Protocol):
    def has_permission(self, actor: Any, action: BoundAction, resource: Any): ...
