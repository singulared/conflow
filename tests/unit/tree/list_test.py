import pytest  # type: ignore
from conflow.node import NodeList, T  # type: ignore


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
