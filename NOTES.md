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
