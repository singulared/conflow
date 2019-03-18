import pytest
from conflow.node import Node, AbstractNode, TK, T


@pytest.mark.parametrize('value,other,representation', [
    ('string', 'otherstring', "Node('test', 'string')"),
    (42, 69, "Node('test', 42)"),
    (42.3, 69.5, "Node('test', 42.3)"),
    (True, False, "Node('test', True)"),
    (None, 1, "Node('test', None)"),
])
def test_node_value(value, other, representation):
    node = Node('test', value)
    assert isinstance(node, AbstractNode)
    assert isinstance(node, Node)
    assert node.value == value
    assert node.value != other
    assert node == value
    assert node != other


@pytest.mark.parametrize('value,representation', [
    ('string', "Node('test', 'string')"),
    (42, "Node('test', 42)"),
    (42.3, "Node('test', 42.3)"),
    (True, "Node('test', True)"),
    (None, "Node('test', None)"),
])
def test_node_repr(value, representation):
    assert repr(Node('test', value)) == representation

