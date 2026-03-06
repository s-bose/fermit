# fermit

Fermit is a policy-as-code library to manage permissions in a declarative way.

## TODO: Open Questions (To be resolved before v1 release)

    1. How would permission scopes work? I.e. `org` or `project` level permissions?
    2. How can we model user/actor entities?
    3. How to model user/actor groups and group permissions?
    4. Do we need explicit Allow/Deny rules? If so, should we support complex conditions for Allow/Deny rules?
    5. How to handle permission conflicts? E.g. if a user has both Allow and Deny permissions for the same action, which one takes precedence?
    6. How to handle permission inheritance? E.g. if a user has permissions for a parent resource, do they automatically get permissions for child resources?
    7. How to model ReBAC, ABAC and other complex access control models? 

## Fundamentals

The core concept in Fermit is the `Resource`. A `Resource` is a class that represents an entity in your system that you want to manage permissions for. Each `Resource` can have multiple `Action`s, which represent the operations that can be performed on that resource.

Resources cannot inherit from other resource.
This is intentional as resources are meant to be self-contained and atomic units of a policy definition.
Relationship between resource actions can be achieved however by `implies` property of `Action`.

This way, `A.create` can imply `B.create` and vice versa but with explicit declaration.

    ```python
    from fermit.core import Resource, Action

    class File(Resource):
        create = Action()
        read = Action(implies=lambda: [Document.read]) # lazy evaluation
        update = Action()
        delete = Action()

    class Document(Resource):
        create = Action()
        read = Action(implies=[File.read])
        update = Action()
        delete = Action()
    ```
