from conflow.dispatcher import Dispatch
from conflow.node import Node, NodeList

dispatch = Dispatch()


@dispatch(Node, Node)
def add(a, b):
    return 'Node - Node'


@dispatch(Node, NodeList)
def add(a, b):
    return 'Node - NodeList'


@dispatch(NodeList, Node)
def add(a, b):
    return 'NodeList - Node'


def test_dispatch():
    base = Node('base', 'node_A')
    other = Node('other', 'node_B')
    assert add(base, other) == 'Node - Node'


def test_dispatch_node_nodelist():
    base = Node('base', 'node_A')
    other = NodeList('other', 'node_B')
    assert add(base, other) == 'Node - NodeList'


def test_dispatch_order():
    base = Node('base', 'node_A')
    other = NodeList('other', 'node_B')
    assert add(other, base) == 'NodeList - Node'
