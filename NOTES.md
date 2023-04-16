# 2022-12-27 02:04:22
pretty barebone decorator working on classes.
Only works with level 0 resources.
What it does not:
1. check whether repeated access values have been put
2. check whether subresources have been added

What stil needs some thought
1. The whole structure of the project
2. How do we design permissions, or give permissions to people?
3. Who do we define by people, are people also resources?

---

# 2022-12-28 02:51:13
`Fermit` should be a module that handles 2 main things

## PART-1) Generating roles
Reads and creates `Roles`, `Permissions` & `Resources` (with something like `FermitGenerator` class)

 * `Roles` are directly tied to an _user_, e.g., **Manager**, **Admin**, **Customer**, etc
 * `Permissions` are tied to both a `Role` as well as a _user_. One user will have one base permission associated with them, upon adding / removing cetain resources from the user, the Permission will change.
 * `Resources` are different predefined components of the system. These are directly tied to an `user`'s permission

Say the input to `Fermit` was

```python

# Each of resources will take up 8 bits
MAX_BIT_PER_RESOURCE = 8

# List of roles
roles = ["admin", "manager", "customer"]

# List of available resources
resources = {
    # The elements in tuple for this resource key is an "access"
    "product": ("create", "edit", "delete", "view")
}

# From about resource declaration the bit sequence .
# for someone who has all access will be something
# like
#
# _   _  _  _   CREATE EDIT DELETE VIEW        # 8 because of MAX_BIT_PER_ACCESS
# 128 64 32 16  8      4    2      1
# ------------------------------------------------------------------------------
# 0   0  0  0   1      1    1      1       =>  15  FOR THE ADMIN
# 0   0  0  0   0      0    0      1       =>   1  FOR THE USER
# 0   0  0  0   0      1    0      1       =>   5  FOR SOMEONE WHO CAN JUST EDIT & VIEW



# These are a sets of base permissions
permissions = {
    "ProductManager": ["product.*"],
    "User": ["product.view"]
}

# Connecting the roles to permissions to the Admin
# (so essentially the accesses as well)
roles = {
    "admin": *, # Has all permission
    "manager": [ProductManager, ...],
    "user": [User]
}

```

Fermit's should be able to create the following 4 tables 

### `Resource`

|id|name|
|:-|:---|
|0|**product**|

### `Access`

|id|name|resource_id|bit_val|
|:-|:---|:----------|:------|
|0|`create`|0|8|
|1|`edit`|0|4|
|1|`delete`|0|2|
|1|`view`|0|1|


### `Permission`

|id|name|resource_fermit_code||
|:-|:---|:-------------------|:-|
|0|__ProductManager__|`7.7.0`||
|1|__OrganizationManager__|`7.7.7`||

### `Roles`

|id|name|permission_id|
|:-|:-|:-|
|0|__admin__|1|
|0|__admin__|2|
|1|__manager__|1|

NOW!! When creating an user first they're assigning a __Predefined Role__, which in turn has a set of __Predefined permissions__ added to them.

### `UserRole`

This is when we've added a base role to an user

|id|user_id|role_id|__comments|
|:-|:-|:-|:-|
|0|`asdagdfh3dfg`|1|_role_id 1 meaning the user is a __manager___|

If the admin now chooses to provide the user the option to see the order details
then his fermit code changes to
```

ORGANIZATION SEQUENCE

_   _  _  _   CREATE EDIT DELETE VIEW        # 8 because of MAX_BIT_PER_ACCESS
128 64 32 16  8      4    2      1
------------------------------------------------------------------------------
0   0  0  0   0      0    0      1           == 1 Meaning can see organization details
```

`7.7.1` from `7.7.0`, which then can be stored at another tabled called

### `UserAdditionalAccess`

|id|user_id|resource_fermit_code||
|:-|:------|:-------------------|:-|
|0|`asdagdfh3dfg`|`0.0.1`||

This table row would be modified everytime a new access is given or revoked to the user. For instance, let's say the manager is now given the scope of editing organization details then his new sequence becomes `0.0.5` (1 for `view` + 4 for `edit`), so the table would now contain this 

|id|user_id|resource_fermit_code||
|:-|:------|:-------------------|:-|
|0|`asdagdfh3dfg`|`0.0.5`||

## 2) Fetching all permissions

The actual `Fermit` class will do this when given an user_id.

+ Input: `user_id`: `asdagdfh3dfg`
+ Fetches the `resource_fermit_code` from `Permission` and `UserAdditionalAccess` table.
+ Will add them (we'll achieve this by overriding `__add__`)
```
  7.7.0 (Taken from Permission)
+ 0.0.5 (Taken from UserAdditionalAccess)
-------
  7.7.5
```
In case of some conflict, such as
```
  7.7.0 (Taken from Permission)
+ 1.4.5 (Taken from UserAdditinoalAccess)
-------
  7.7.5 (Priority given to the base permission with the highest bit value)
```
+ Finally it accesses based on these sequence and returns a list like so `product.create`, `product.edit`, etc (format `RESOURCE.ACCESS`)

---

# 2022-12-28 17:42:48

## Notes about implementation details
The notes above describe the structurre in the form of db tables, which can be implemented easily.
The main question is, will fermit be a no-db solution by default? or db-only by default?

#### 1. No-db solution
We need to have a Fermit core class which can be instantiated as a single entrypoint.
All resources/roles/permissions defined will have to be latched onto that.

Different fermit instances will be completely isolated containers with their separate IAM config.

#### 2. db solution
We can bind these two together. So that the Fermit class can be optionally passed the db dsn for it
to connect to and create the necessary tables.
 
## Open Questions
1. What should we do with sub-resources?
Is a sub-resource always bound to its parent resource?
In that case, you cannot give someone direct permission to the sub-resource.
Example:

resource A: {"add", "edit", "delete", "B.add", "B.delete"}

\# resource C trying to have access to B:

resource C: {"add", "edit", "A.add", "A.edit", "A.B.add", "A.B.delete"}

Ans. subresources will be bound to its parent resource.
Meaning. `A.B.add` is different from `C.B.add`



## 2023-04-16 18:41:09 
### New Details

We have to add a sort of controller level decorator for each endpoint in FastAPI.
Such as below:

```python

from fastapi import APIRouter, Security
from app.permissions.resources import Item # assuming the following structure
# - app
#   - permissions
#     - resources.py -> class item(fermit.Resource)
from app.crud.item import item_service

item_route = APIRouter("/item")

@item_route.post("/")
async def post_item(*, current_user = Security(get_current_user), scopes=[Item.read, Item.create], item: ItemCreate):
  if item := await item_service.get(item.id):
    raise HTTPException(400, "item already exists")
  item_new = await item_service.create(**item.dict())
  return item_new
```

For setting all the scopes you have to import all the resources inside your scope.
By default all the resource objs have a `__repr__` that will generate the composed string that covers all the acls into a conclusive integer.
Such as, if there's a resource A: {create, read, update, delete, B.create, B.read, B.delete} then the string repr for A is:
```
create : 1
read   : 2
update : 4
delete : 8
B.create : 16
B.read : 32
B.update : 64

TOTAL : 127
```
So when we do `repr(A)`, or `A.value`, we will get `127`, and `A.desc` will give us a dictionary of the individual acs:
```python
{
  "A.create": 1,
  "read"   : 2,
  "update" : 4,
  "delete" : 8,
  "B.create" : 16,
  "B.read" : 32,
  "B.update" : 64,
}
```

Thus, when we want to initialize our fastapi oauth2_scheme with the scopes, we will have to add all the resouce scopes at one place.
We can do it in this way:

```python
from app.permissions.resources import *


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="api/v1/user/token",
    scopes={A.name: A.value, X.name: X.value, some_other_res.name: some_other_res.value}, # scopes receive a dict with resource name as key, and its description as value
)
```

or, if we can use fermit to ease this process.

```python

from fermit.utils import generate_scope
from app.permissions import resources

scopes = generate_scope(resources)
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="api/v1/user/token", 
    scopes=scopes
)
```

Once the scopes are set, we now come to the part where we authenticate users. But before that we need to know how are they getting the permissions in the first place which we will validate later. For that we will use JWT tokens.

```python
from app.permissions import roles # Roles are defined as followed:
'''
from fermit import Role
from app.permissions.resources import A, B, C

# app/permissions/roles.py

class User(Role):
  permissions = [
    A.create,
    A.read,
    B.create,
    B.read
  ]

class Admin(Role):
  permissions = [
    A.*,
    B.*,
    C.*
  ]
'''
from fermit.utils import get_permissions_for_role
from app.permissions import roles

@app.post("/api/v1/user/register")
async def register_user(username: str, password: str):
  return await user_svc.create_user(username, password, role=roles.User)


@app.post("/api/v1/user/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await user_svc.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    permissions: dict[str, int] = get_permissions_for_role(user.role) 
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": permissions},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}
```

To authenticate a logged in user's JWT token, we need a dependency, as followed:

```python
from fermit.utils import validate_permissions

async def get_current_user(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
        
        validate_permissions(scope, token_data.scopes[scope])

    return user
```


To create an authenticated endpoint, we proceed as followed:

```python
from fermit.utils import get_permissions_for_role
from app.permissions.roles import User

@route.get("/analytics")
async def get_analytics(
  current_user = Security(
    get_current_user, 
    scopes=[get_permissions_for_role(User)]
    )
):
  ...

# this will enable RBAC-based auth
```

This is an example of RBAC-enabled auth where permissions are clustered into designated roles and the login flow and access control for endpoints is also specific to roles.

However, should the need arise, there is also a way to do this on a permission-level. As followed:

```python
from app.permissions.resources import analytics

@route.get("/analytics")
async def get_analytics(
  current_user = Security(
    get_current_user, 
    scopes=[analytics.read]
    )
):
  ...


@route.post("/analytics")
async def get_analytics(
  current_user = Security(
    get_current_user, 
    scopes=[analytics.read, analytics.create]
    )
):
  ...
```