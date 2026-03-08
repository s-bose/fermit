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

### Resource

The core concept in Fermit is the `Resource`. A `Resource` is a class that represents an entity in your system that you want to manage permissions for. Each `Resource` can have multiple `Action`s, which represent the operations that can be performed on that resource.
Resources are the most fundamental concept in Fermit. They represent a single source-of-truth for containing all the actions permitted on that resource.

### Action

Actions are defined with the function `Action()` which binds an action instance to a resource.
Actions are always tied to a specific resource and represent the operations that can be performed on that resource. For example, if you have a `Document` resource, you might have actions like `read`, `write`, and `delete`.

Actions are internally represented and valuated as incrementing integers ordered by their declaration order. This allows for efficient permission checks using bitwise operations.

### Relationships

Relationships are declaration primitive to define how resources are related to each other.
For example, in a Github-like system you might have a `Repository` resource and a `Folder` resource.
Where `Folder` can be related to a `Repository`.

It can be defined as followed:

    ```python
    class Repository(Resource):
        read = Action()
        write = Action()
        delete = Action()

    class Folder(Resource):
        read = Action()
        write = Action()
        delete = Action()

        repository = Relation(Repository) # relationship_name = Relation(related_resource_class)
    ```
