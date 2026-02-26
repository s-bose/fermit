from __future__ import annotations

from typing import Callable

from mypy.nodes import (
    AssignmentStmt,
    CallExpr,
    MemberExpr,
    NameExpr,
    StrExpr,
    TupleExpr,
    TypeInfo,
    Var,
)
from mypy.plugin import ClassDefContext, Plugin
from mypy.plugins.common import add_attribute_to_class
from mypy.types import Instance

RESOURCE_FULLNAME = "fermit.core.resource.Resource"
BOUND_ACTION_FULLNAME = "fermit.core.action.BoundAction"
ACTION_FULLNAME = "fermit.core.action.Action"

def _get_bound_action_type(ctx: ClassDefContext) -> Instance | None:
    """Look up the BoundAction type in the current semantic analysis context."""
    sym = ctx.api.lookup_fully_qualified_or_none(BOUND_ACTION_FULLNAME)
    if sym is None or sym.node is None:
        return None
    return Instance(sym.node.info, []) if hasattr(sym.node, "info") else None


def _extract_action_names(ctx: ClassDefContext) -> list[str]:
    """
    Parse the `actions = (...)` assignment and extract action names.
    Handles both plain strings and Action(name="...") calls.
    """
    names: list[str] = []

    for stmt in ctx.cls.defs.body:
        if not isinstance(stmt, AssignmentStmt):
            continue
        if len(stmt.lvalues) != 1:
            continue

        lvalue = stmt.lvalues[0]
        if not isinstance(lvalue, (NameExpr, MemberExpr)):
            continue
        if isinstance(lvalue, NameExpr) and lvalue.name != "actions":
            continue
        if isinstance(lvalue, MemberExpr) and lvalue.name != "actions":
            continue

        rvalue = stmt.rvalue
        if not isinstance(rvalue, TupleExpr):
            continue

        for item in rvalue.items:
            # Case 1: plain string — "create"
            if isinstance(item, StrExpr):
                names.append(item.value)

            # Case 2: Action(name="create", ...) or Action("create", ...)
            elif isinstance(item, CallExpr):
                name = _extract_name_from_action_call(item)
                if name is not None:
                    names.append(name)

    return names


def _extract_name_from_action_call(call: CallExpr) -> str | None:
    """Extract the `name` argument from an Action(...) call."""
    # Positional first arg: Action("create")
    if call.args and isinstance(call.args[0], StrExpr):
        # Check if it's the first positional or name= keyword
        if not call.arg_names[0] or call.arg_names[0] == "name":
            return call.args[0].value

    # Keyword: Action(name="create")
    for arg_name, arg_value in zip(call.arg_names, call.args):
        if arg_name == "name" and isinstance(arg_value, StrExpr):
            return arg_value.value

    return None

def _resource_class_hook(ctx: ClassDefContext) -> None:
    """
    For each Resource subclass, read `actions` and synthesize
    class attributes typed as BoundAction.
    """
    bound_action_type = _get_bound_action_type(ctx)
    if bound_action_type is None:
        return

    action_names = _extract_action_names(ctx)

    for name in action_names:
        attr_name = name
        add_attribute_to_class(
            api=ctx.api,
            cls=ctx.cls,
            name=attr_name,
            typ=bound_action_type,
            is_classvar=True,
        )


class ResourcePlugin(Plugin):
    def get_base_class_hook(
        self, fullname: str
    ) -> Callable[[ClassDefContext], None] | None:
        if fullname == RESOURCE_FULLNAME:
            return _resource_class_hook
        return None

def plugin(version: str) -> type[Plugin]:
    return ResourcePlugin