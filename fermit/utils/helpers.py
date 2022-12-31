from typing import Optional, List, Any
import re
from itertools import groupby

def find_subresource_string(string: str) -> Optional[str]:
    match = re.match(r"\w+\.\w+(\.\w+)+", string)
    if match:
        return match.group(0)
    return None

def split_resource_string(string: str) -> List[str]:
    return string.split(".")

def split_access_strings(acl: List[str]) -> List[Any]:
    acl_split = [acs.split(".") for acs in acl_split]
    groupby(sorted(acl_split, key=len), key=len)
