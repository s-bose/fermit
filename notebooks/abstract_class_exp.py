import marimo

__generated_with = "0.20.2"
app = marimo.App(width="medium")


@app.cell
def _():
    from typing import ClassVar
    from fermit.core.action import Action, ActionSet, BoundAction
    from fermit.core.resource import Resource

    class Role:
        permissions: ClassVar[list[BoundAction, ActionSet]]



    return Action, Resource, Role


@app.cell
def _(Action, Resource, Role):
    class Product(Resource):
        create = Action()
        delete = Action()

    class User(Role):
        permissions = [Product.all]

    User.permissions
    return


@app.cell
def _():
    from enum import Enum

    class Foo(Enum):
        bar = "bar"
        baz = "baz"


    for v in Foo:
        print(v.value)
    return


@app.cell
def _():
    import ast


    x = ast.FunctionDef(
        name="foo",
        args=ast.arguments(
            posonlyargs=[],
            args=[
                ast.arg(
                    arg="bar"
                )
            ]
        ),
        body=[
            ast.Return(value=ast.Constant(1))
        ]
    )
    return ast, x


@app.cell
def _(ast, x):
    module = ast.Module(body=[x])
    ast.fix_missing_locations(module)
    code = compile(module, "<foo>", "exec")
    bin = exec(code, {"foo": 123})

    print(code)
    return (code,)


@app.cell
def _(code):
    import dis

    dis.dis(code.co_code)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
