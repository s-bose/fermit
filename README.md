# fermit

Fermit is a policy-as-code library to manage permissions in a declarative way.

## Fundamentals

The core concept in Fermit is the `Resource`. A `Resource` is a class that represents an entity in your system that you want to manage permissions for. Each `Resource` can have multiple `Action`s, which represent the operations that can be performed on that resource.

Resources can inherit from other resource, and they will inherit all the actions of the parent resource.
However, actions for each resource are unique to that resource only. For example, if you have a `File` resource, and a `Product` resource, the actions for `File` will not affect the actions for `Product`.

```python
from fermit.core import Resource, Action

class File(Resource):
    create = Action()
    read = Action()
    update = Action()
    delete = Action()

class Product(File):
    create = Action()
    read = Action()
    update = Action()
    delete = Action()
```

Here `Product` embeds `File`, not directly inherit.
So the actions for Product are defined as follows:
    - #0 - File.create
    - #1 - File.read
    - #2 - File.update
    - #3 - File.delete
    - #4 - Product.create
    - #5 - Product.read
    - #6 - Product.update
    - #7 - Product.delete
To access the File actions, you can use `Product.File.create`, `Product.File.read`, etc.