from typing import List, Dict

from fermit.app.resource import Resource

class Fermit:

    def __init__(self):
        self.resources = []
    
    def add_resources(self, resouces: Dict[str, List[str]]):
        """
        example resource list:
        {
            "product": ["add", "delete", "create"],
            "sales": ["add", "delete", "analytics.add", "analytics.delete"],
        }

        could also be defined in json
        """

        resouces_list = []
        
        for name, acl in resouces.items():
            resouces_list.append(Resource(name=name, access_list=acl))

        self.resources = resouces_list

