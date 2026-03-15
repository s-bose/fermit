import pytest

from fermit.core import Resource
from fermit.core.action import Action
from fermit.core.role import Role


def test_role_creation():
    class Admin(Role):
        name = "admin"
        description = "Administrator role with all permissions"
        permissions = []

    assert not Admin.permissions
    assert Admin.name == "admin"


def test_role_inheritance():

    class Repository(Resource):
        read = Action()
        create = Action()
        delete = Action()

    class Organisation(Resource):
        read = Action()
        create = Action()
        delete = Action()

    class User(Role):
        name = "user"
        description = "Administrator role with all permissions"
        permissions = [Repository.read, Repository.create]

    class Admin(User):
        name = "admin"
        description = "Regular user role with limited permissions"
        permissions = [Organisation.all()]

    assert Admin.name == "admin"
    assert User.name == "user"
    assert Repository.read in Admin.permissions


def test_role_permissions():
    class Repository(Resource):
        read = Action()
        create = Action()
        delete = Action()

    class Organisation(Resource):
        read = Action()
        create = Action()
        delete = Action()

    class User(Role):
        name = "user"
        description = "Administrator role with all permissions"
        permissions = [Repository.read, Repository.create, Organisation.all()]

    assert Repository.read in User.permissions
    assert Repository.delete not in User.permissions
    assert Organisation.read in User.permissions


def test_role_scopes_all():
    class Repository(Resource):
        read = Action()
        create = Action()
        delete = Action()

    class Organisation(Resource):
        read = Action()
        create = Action()
        delete = Action()

    class User(Role):
        name = "user"
        description = "Administrator role with all permissions"
        permissions = [Repository.read, Repository.create, Organisation.all()]
        scopes = "*"

    assert Repository.read in User.permissions
    assert Repository.delete not in User.permissions
    assert Organisation.read in User.permissions

    assert Repository in User.get_scopes()
    assert Organisation in User.get_scopes()


def test_role_specific_scopes():
    class Repository(Resource):
        read = Action()
        create = Action()
        delete = Action()

    class Organisation(Resource):
        read = Action()
        create = Action()
        delete = Action()

    class User(Role):
        name = "user"
        description = "Administrator role with all permissions"
        permissions = [Repository.read, Repository.create, Organisation.all()]
        scopes = [Repository]

    assert Repository.read in User.permissions
    assert Repository.delete not in User.permissions
    assert Organisation.read in User.permissions

    assert Repository in User.get_scopes()
    assert Organisation not in User.get_scopes()


def test_role_invalid_scope():
    class Repository(Resource):
        read = Action()
        create = Action()
        delete = Action()

    class Organisation(Resource):
        read = Action()
        create = Action()
        delete = Action()

    class Account(Resource):
        read = Action()
        create = Action()
        delete = Action()

    with pytest.raises(ValueError):

        class _(Role):
            name = "user"
            description = "Administrator role with all permissions"
            permissions = [Repository.read, Repository.create, Organisation.all()]
            scopes = [Account]  # Invalid scope
