from fermit.core import Action, Resource
from fermit.core.relation import Relation
from fermit.core.role import Role


class Repository(Resource):
    create = Action()
    read = Action()
    update = Action()
    delete = Action()

    roles = {
        "user": Role(permissions=[read, create, update]),
        "admin": Role(
            permissions=[create, read, update, delete],
        ),
    }


class Folder(Resource):
    create = Action()
    read = Action()
    update = Action()
    delete = Action()

    parent = Relation(Repository)

    roles = {
        "user": Role(
            permissions=[read, create, update],
        ),
        "admin": Role(
            permissions=[create, read, update, delete],
        ),
    }


## Roles


class User(Role):
    permissions = [
        Repository.read,
        Repository.create,
        Repository.update,
    ]


class Admin(User):
    permissions = [
        Repository.delete,
        Folder.create,
        Folder.read,
        Folder.update,
        Folder.delete,
    ]

    scopes = "*"
