from typing import Optional, List, Any
import re
from collections import defaultdict
from itertools import groupby

def find_subresource_string(string: str) -> Optional[str]:
    match = re.match(r"\w+\.\w+(\.\w+)+", string)
    if match:
        return match.group(0)
    return None

def split_resource_string(string: str) -> List[str]:
    return string.split(".")


def gen_resource_cluster_from_acl(lst: List[str]) -> dict:
    _dict = defaultdict(list)

    for acs in lst:
        *prefix, verb = acs.split(".")
        if not prefix:
            _dict["."].append(verb)
        else:
            obj = _dict
            for bit in prefix:
                obj = obj.setdefault(bit, defaultdict(list))
            obj["."].append(verb)



    def default_to_regular(_dict: defaultdict):
        if isinstance(_dict, defaultdict):
            _dict = {k: default_to_regular(v) for k, v in _dict.items()}
        return _dict
    
    return default_to_regular(_dict)
