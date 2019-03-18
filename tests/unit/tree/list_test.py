import pytest  # type: ignore
from conflow.node import NodeList, T, Node  # type: ignore


@pytest.mark.parametrize('value,representation', [
    ([1, 2, 3], "NodeList('test', [1, 2, 3])"),
    ([42, 3.3, 'abc'], "NodeList('test', [42, 3.3, 'abc'])"),
])
def test_node_list(value: T, representation: str) -> None:
    node = NodeList('test', value)
    assert repr(node) == representation
    assert node == value
    assert node != ['missing value']
    for el in value:
        assert el in node
    assert len(node) == len(value)
    assert 'missing value' not in node


def test_list_iterator():
    values = [1, 2.0, 'str', None]
    node_list = NodeList('test', values)
    for i, node in enumerate(node_list):
        assert isinstance(node, Node)
        assert node == values[i]


def test_list_item():
    values = [1, 2.0, 'str', None, 'last_value']
    node_list = NodeList('test', values)
    for i in range(len(node_list)):
        node = node_list[i]
        assert isinstance(node, Node)
        assert node == values[i]
    with pytest.raises(IndexError):
        node_list[42]
    assert node_list[-1] == values[-1]


def test_list_value():
    values = [1, 2.0, 'str', None, 'last_value']
    node_list = NodeList('test', values)
    assert node_list.value == values
