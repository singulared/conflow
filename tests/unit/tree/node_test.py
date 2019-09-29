import pytest
from conflow.node import Node, AbstractNode


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
    assert node() == value
    assert node() != other
    assert node == value
    assert node != other


@pytest.mark.parametrize('value', [
    'string', 42, 42.3, True, None,
])
def test_node_missing_getattr(value):
    assert Node('test', value).missing.missingtoo == Node('missingtoo', None)


@pytest.mark.parametrize('value,representation', [
    ('string', "Node('test', 'string')"),
    (42, "Node('test', 42)"),
    (42.3, "Node('test', 42.3)"),
    (True, "Node('test', True)"),
    (None, "Node('test', None)"),
])
def test_node_repr(value, representation):
    assert repr(Node('test', value)) == representation
