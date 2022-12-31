from uuid import UUID, uuid4
from typing import Tuple, Dict, Any, List
from pydantic import BaseModel, Field, root_validator

class Resource(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    access_list: List[str]

    @root_validator()
    def resource_validation(cls, values: Dict[str, Any]):
        acl = values.get("access_list")
        acl = [acs.lower() for acs in acl]

        if len(acl) != len(set(acl)):
            raise ValueError("cannot have duplicate access values")
        
        values["access_list"] = acl
        values["name"] = values.get("name").lower()

        # for index, acs in enumerate(acl):
        #     acs_values = acs.split(".")
            # if len(acs_values) > 1:
                # subresource


        return values
