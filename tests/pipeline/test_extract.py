import pytest
import json

import src.pipeline.extract as extract

@pytest.fixture
def config_fixture():
    with open("systemConfig/testSystem.json", "r") as f:
        return json.loads(f.read())

def test_get_file(config_fixture):
    assert len(extract.get(config_fixture))

def test_get_fileOrders(config_fixture):
    orders = [
        24362720,
        25343668,
        27616557,
        27658628,
        27658628,
        27823496,
        27846052,
        28079578,
        28461300,
        28498422,
        28866496,
        29636861,
        29742707,
        29764332,
        30145344,
        31513216,
        31628442,
        31670302,
        31706238,
        31709410
    ]
    assert extract.get(config_fixture)["OrderId"].to_list() == orders