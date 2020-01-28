import pytest  # type: ignore
from typing import Dict
from conflow.node import NodeMap, Node, AbstractNode  # type: ignore


FLAT_VALUES = [
    {'a': 'b', 'b': 'c', 'd': 'e'},
    {'str': 'str', 'int': 123, 'float': 3.14, 'None': None},
]

NESTED_VALUES = [
    {
        'nested': {
            'list': [1, 2, 3],
            'map': {'a': 'a'}
        }
    }
]

ATTRIBUTE_ERROR_VALUES = [
    {1: 321},
    {None: 123},
    {3.14: 0},
]


@pytest.mark.parametrize('value', FLAT_VALUES + ATTRIBUTE_ERROR_VALUES)
def test_node_map(value: Dict) -> None:
    node = NodeMap('test', value)
    assert node == value
    assert node != {'missing key': None}
    assert len(node) == len(value)
    assert 'missing key' not in node


@pytest.mark.parametrize('value', NESTED_VALUES)
def test_node_map_nested(value: Dict) -> None:
    representation = (
        "NodeMap('test', {'nested': {'list': [1, 2, 3], 'map': {'a': 'a'}}})"
    )
    node = NodeMap('test', value)

    assert repr(node) == representation
    assert node == value

    assert node['nested'] == value['nested']
    assert node['nested']['list'] == value['nested']['list']
    assert node['nested']['map'] == value['nested']['map']

    assert node.nested() == value['nested']
    assert node.nested.list() == value['nested']['list']
    assert node.nested.map() == value['nested']['map']
    assert node.nested.map.a() == value['nested']['map']['a']


@pytest.mark.parametrize('value', NESTED_VALUES)
def test_node_map_nested_missed_chain(value: Dict) -> None:
    node = NodeMap('test', value)
    assert node.missing.missing() is None
    assert node.nested.map.missing() is None
    with pytest.raises(KeyError):
        node.nested.map['missing']


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


@pytest.mark.parametrize('value', FLAT_VALUES + ATTRIBUTE_ERROR_VALUES)
def test_map_repr(value):
    node = NodeMap('test', value)
    assert repr(node), repr(value)


@pytest.mark.parametrize('value', FLAT_VALUES + ATTRIBUTE_ERROR_VALUES)
def test_map_value(value):
    node = NodeMap('test', value)
    assert node(), value
    for k in value:
        assert node[k]() == value[k]


@pytest.mark.parametrize('value', NESTED_VALUES)
def test_map_delete(value):
    node = NodeMap('test', value)
    del(node['nested']['list'])
    assert len(node.nested) == 1
