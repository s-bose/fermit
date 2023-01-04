from uuid import UUID, uuid4
from typing import Tuple, Dict, Any, List
from pydantic import BaseModel, Field, root_validator

from fermit.utils.helpers import gen_resource_cluster_from_acl

class Resource(BaseModel):
    """
    pydantic class for defining a resource.

    Fields
    ------
    - name : name of the resource
    - acl : access control list
    acl strings will get parsed to create a 
    resource-subresource hierarchy to generate
    the access values for each of the access strs.
    """
    id: UUID = Field(default_factory=uuid4)
    name: str
    acl: List[str]

    @root_validator()
    def resource_validation(cls, values: Dict[str, Any]):
        acl = values.get("acl")
        acl = [acs.lower() for acs in acl]

        if len(acl) != len(set(acl)):
            raise ValueError("cannot have duplicate access values")
        
        values["acl"] = acl
        values["name"] = values.get("name").lower()
        values["resource_cluster"] = gen_resource_cluster_from_acl(acl)
        return values

    def __parse_evaluate_cluster(self, cluster: dict):
        """
        a cluster for an acl 
        ["add", "delete", "edit", "a.add", "a.delete", "c.add", "a.edit", "a.b.add", "a.b.edit", "a.b.d.edit"]
        will look like this:
        
        {
            '.': ['add', 'delete', 'edit'],
            'a': {
                '.': ['add', 'delete', 'edit'],
                'b': {
                    '.': ['add', 'edit'],
                    'd': {'.': ['edit']
                    }
                }
            },
            'c': {'.': ['add']}
        }
        """