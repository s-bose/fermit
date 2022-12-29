from typing import Tuple, Dict, Any
from pydantic import BaseModel, root_validator

class Resource(BaseModel):
    name: str
    access_list: Tuple[str]

    @root_validator(pre=True)
    def resource_validation(cls, values: Dict[str, Any]):
