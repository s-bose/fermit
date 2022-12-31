import pytest
from pydantic import ValidationError
from fermit.app.resource import Resource


def test_create_good_resource():
    resource = Resource(name="abc", access_list=["add", "delete", "edit"])
    
