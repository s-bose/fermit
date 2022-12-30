from typing import Tuple, Dict, Any, List
from pydantic import BaseModel, root_validator

class Resource(BaseModel):
    name: str
    access_list: Tuple[str]

    @root_validator(pre=True)
    def resource_validation(cls, values: Dict[str, Any]):
        acl = values.get("access_list")
        acl = (acs.lower() for acs in acl)

        if len(acl) != len(set(acl)):
            raise ValueError("cannot have duplicate access values")



    @classmethod
    def add_resources(cls, resources: List[Dict[str, Tuple[str]]]):
        """utility function to add multiple resources in a list
        of dict format.
        """


