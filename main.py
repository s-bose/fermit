from fermit.core.action import Action
from fermit.core.resource import Resource


class Product(Resource):
    read = Action()
    create = Action(description="Create a new product", aliases=("c", "create"))
    update = Action(description="Update an existing product", aliases=("u", "update"))
    delete = Action(description="Delete an existing product", serialize_as="product -> rm")


if __name__ == "__main__":
    print(Product.read.value)
    print(Product.create.value)
    print(Product.update.value)
    print(Product.delete.value)
