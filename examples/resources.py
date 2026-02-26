from fermit import Action, Resource, Role


class Product(Resource):
    create = Action()
    read = Action()
    update = Action()
    delete = Action()


class Order(Resource):
    create = Action()
    read = Action()
    cancel = Action()


class Manager(Role):
    permissions = [
        Product.create,
        Product.read,
        Product.update,
        Order.read,
    ]


from fermit import Resource, Action, Role

class Product(Resource):
    create = Action()
    read   = Action()
    update = Action()
    delete = Action()

class Order(Resource):
    create = Action()
    read   = Action()
    cancel = Action()

class Manager(Role):
    permissions = [
        Product.create, Product.read, Product.update,
        Order.read,
    ]


from fermit import Role, Group

class Developer(Role):
    permissions = [Product.read, Product.update, Order.read]

class Deployer(Role):
    permissions = [Pipeline.create, Pipeline.read, Pipeline.delete]

class Engineering(Group):
    roles = [Developer, Deployer]

# Engineering compiles to:
#   Product:  read | update  = 0b0110
#   Order:    read           = 0b0010
#   Pipeline: create | read | delete = 0b1011


from fermit import Policy, Condition

class OwnOrdersOnly(Policy):
    """Users can only read/update orders they own."""
    resource = Order
    actions = [Order.read, Order.update]
    condition = Condition(
        resource_attr="owner_id",
        operator="eq",
        subject_attr="user_id",
    )

class SameTenantProducts(Policy):
    """Users can only access products within their tenant."""
    resource = Product
    actions = [Product.read, Product.update, Product.delete]
    condition = Condition(
        resource_attr="tenant_id",
        operator="eq",
        subject_attr="tenant_id",
    )
