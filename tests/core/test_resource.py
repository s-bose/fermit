import pytest
from fermit.core import Action
from fermit.core.resource import Resource


def test_resource_cannot_be_instantiated():

    class Product(Resource):
        pass

    with pytest.raises(TypeError):
        Product()


def test_resource_cannot_inherit_from_another_resource():
    class Fruit(Resource):
        pass

    with pytest.raises(TypeError):

        class _(Fruit):
            pass


def test_resource_bound_action_position():
    class File(Resource):
        create = Action()
        read = Action()
        delete = Action()

    assert File.create.position == 0
    assert File.read.position == 1
    assert File.delete.position == 2


def test_resource_bound_action_aliases():
    class File(Resource):
        create = Action(aliases=("add", "new"))
        read = Action()
        delete = Action()

    assert File.create.position == 0
    assert File.read.position == 1
    assert File.delete.position == 2

    assert File.create.aliases == ("add", "new")
    assert File.add is File.create
    assert File.new is File.create


def test_resource_bound_action_aliases_conflict():
    with pytest.raises(ValueError):

        class _(Resource):
            create = Action(aliases=("add", "new"))
            read = Action()
            delete = Action(aliases=("add",))


def test_resource_enum_classes_can_be_instantiated_as_bound_actions():
    class File(Resource):
        create = Action()
        read = Action()
        delete = Action()

    assert File("create") is File.create


def test_resource_mask():
    class File(Resource):
        create = Action()
        read = Action()
        delete = Action()

    class Product(Resource):
        create = Action()
        read = Action()

    assert File.create.mask() == 1 << 0
    assert File.read.mask() == 1 << 1
    assert File.delete.mask() == 1 << 2

    assert File.mask() == File.mask("*") == (1 << 3) - 1

    assert (
        File.mask([File.create, File.delete]) == File.create.mask() | File.delete.mask()
    )

    with pytest.raises(ValueError):
        File.mask([File.create, Product.create])


def test_resource_implied_actions():
    class File(Resource):
        read = Action()
        create = Action()
        read = Action()
        delete = Action(implies=lambda: [Document.delete])

    class Document(Resource):
        read = Action(implies=[File.read])
        create = Action(implies=[File.create])
        delete = Action(implies=lambda: [File.delete])

    assert Document.read.implied_actions() == frozenset([File.read])
    assert Document.create.implied_actions() == frozenset([File.create])
    assert Document.delete.implied_actions() == frozenset([File.delete])

    assert File.delete.implied_actions() == frozenset([Document.delete])
