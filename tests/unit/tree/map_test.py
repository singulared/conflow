import pytest  # type: ignore
from typing import Dict
from conflow.node import NodeMap, Node, AbstractNode  # type: ignore


FLAT_VALUES = [
    {'a': 'b', 'b': 'c', 'd': 'e'},
    {'str': 'str', 'int': 123, 'float': 3.14, 'None': None},
]

ATTRIBUTE_ERROR_VALUES = [
    {1: 321},
    {None: 123},
    {3.14: 0},
    {(1, 2): (3, 4)},
]


@pytest.mark.parametrize('value', FLAT_VALUES + ATTRIBUTE_ERROR_VALUES)
def test_node_map(value: Dict) -> None:
    node = NodeMap('test', value)
    assert node == value
    assert node != {'missing key': None}
    assert len(node) == len(value)
    assert 'missing key' not in node


@pytest.mark.parametrize('value', FLAT_VALUES + ATTRIBUTE_ERROR_VALUES)
def test_map_getitem(value):
    node = NodeMap('test', value)
    for k in value:
        assert k in node
        assert node[k] == value[k]
        assert isinstance(node[k], Node)
        assert isinstance(node[k], AbstractNode)


@pytest.mark.parametrize('value', FLAT_VALUES)
def test_map_getattribute(value):
    node = NodeMap('test', value)
    for k in value:
        assert k in node
        assert getattr(node, k) == value[k]
        assert isinstance(getattr(node, k), Node)
        assert isinstance(getattr(node, k), AbstractNode)


@pytest.mark.parametrize('value', ATTRIBUTE_ERROR_VALUES)
def test_map_getattribute_error(value):
    node = NodeMap('test', value)
    for k in value:
        assert k in node
        with pytest.raises(TypeError):
            assert getattr(node, k) == value[k]