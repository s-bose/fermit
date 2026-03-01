from asyncio import PriorityQueue
import pytest
from fermit.core import Action
from fermit.core.resource import Resource


def test_resource_cannot_be_instantiated():

    class Product(Resource):
        pass

    with pytest.raises(TypeError):
        Product()


def test_resource_inheritance():
    class File(Resource):
        create = Action()
        read = Action()
        delete = Action()

    class Product(File):
        create = Action()
        update = Action()

    assert Product.create is not File.create
    assert Product.read is File.read
    assert Product.delete is File.delete

    assert Product.create.position == 0
    assert Product.read.position == 1
    assert Product.delete.position == 2
    assert Product.update.position == 3

    assert Product.mask == (1 << 4) - 1
