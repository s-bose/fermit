from typing import Callable, Any, Tuple, List, Optional
import re
from dataclasses import dataclass

def find_subresource_string(string: str) -> Optional[str]:
    match = re.match(r"\w+\.\w+(\.\w+)+", string)
    if match:
        return match.group(0)
    return None

def split_resource_string(string: str) -> List[str]:
    return string.split(".")


# day 1: start small, only work for level 0 resources
class Resource:
    def __init__(self, name: str) -> None:
        self.name = name

    def __call__(self, cls=None, *args, **kwargs):
        def wrapper(cls):
            access_list: Tuple[str] = getattr(cls, "__access__")
            if access_list is None:
                raise ValueError("A resource must have an __access__ field")
            
            access_values = {}
            for idx, value in enumerate(access_list):
                access_values[value] = 1 << idx
            
            resource_value = sum(access_values.values())
            setattr(cls, "resource_value", resource_value)
            setattr(cls, "access_values", access_values)

            return cls

        if cls is None:
            return wrapper

        return wrapper(cls)



