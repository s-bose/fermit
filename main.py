from fermit.core.resource import Resource
from fermit.core.action import Action


class Product(Resource):
    read = Action()
    create = Action(description="Create a new product", aliases=("c", "create"))
    update = Action(description="Update an existing product", aliases=("u", "update"))
    delete = Action(description="Delete an existing product")


if __name__ == "__main__":
    print(Product.read)
    print(Product.create)
    print(Product.update)
    print(Product.delete)
