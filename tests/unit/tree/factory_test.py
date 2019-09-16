import pytest
from conflow.node import node_factory, AbstractNode, Node, NodeList, NodeMap


@pytest.mark.parametrize('value,type', [
    ('string', Node),
    (42, Node),
    (42.3, Node),
    (True, Node),
    (None, Node),
    ([], NodeList),
    ({}, NodeMap),
])
def test_node_value(value, type):
    node = node_factory('test', value)
    assert isinstance(node, AbstractNode)
    assert isinstance(node, type)
