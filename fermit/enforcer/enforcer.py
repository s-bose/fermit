from typing import Any, Protocol, runtime_checkable

from fermit.core.meta import BoundAction


class PolicyEnforcer(Protocol):
    def has_permission(self, actor: Any, action: BoundAction, resource: Any): ...
