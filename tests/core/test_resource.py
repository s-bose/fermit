import pytest

from fermit.core import Action
from fermit.core.relation import Relation
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

    assert File.mask([File.create, File.delete]) == File.create.mask() | File.delete.mask()

    with pytest.raises(ValueError):
        File.mask([File.create, Product.create])


def test_resource_relationship():
    class Repository(Resource):
        read = Action()
        write = Action()

    class Folder(Resource):
        read = Action()
        write = Action()
        delete = Action()

        repository = Relation(Repository)

    class File(Resource):
        read = Action()
        write = Action()

        repository = Relation(Repository, name="file_repository", description="File belongs to Repository")

        folder = Relation(Folder, description="File belongs to Folder")

    assert File.repository.target is Repository
    assert File.repository.name == "file_repository"
    assert File.file_repository.target is Repository
    assert File.repository.description == "File belongs to Repository"
    assert File.folder.target is Folder
    assert File.folder.name == "folder"
    assert File.folder.description == "File belongs to Folder"


def test_resource_action_setname():
    class File(Resource):
        create = Action(description="Create a file")
        read = Action(name="read123", description="Read a file")

    assert File.create.name == "create"
    assert File.read.name == "read123"


def test_resource_with_roles():
    from fermit.core.role import Role

    class File(Resource):
        create = Action()
        read = Action()
        delete = Action()

        roles = {
            "editor": Role(
                permissions=[create, read],
            ),
            "admin": Role(
                name="Administrator",
                permissions=[create, read, delete],
            ),
        }

    assert "editor" in File.roles
    assert "admin" in File.roles

    assert File.roles["editor"].name == "editor"
    assert File.roles["admin"].name == "Administrator"

    assert File.read in File.roles["editor"].permissions
    assert File.create in File.roles["editor"].permissions
    assert File.delete not in File.roles["editor"].permissions

    assert File.read in File.roles["admin"].permissions
    assert File.create in File.roles["admin"].permissions
    assert File.delete in File.roles["admin"].permissions
