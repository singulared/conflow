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


'''
@pytest.mark.skip
def test_confignode_in(config_node_data):
    node = Node('test', config_node_data['dict'])
    assert 'int' in node
    assert 'list' in node
    assert 'none' in node
    assert 'missing' not in node


@pytest.mark.xfail
def test_confignode_repr(config_node_data):
    node = Node('test', config_node_data)
    assert repr(node) == 'Node(\'test\', {})'.format(config_node_data)


@pytest.mark.xfail
def test_confignode_getitem(config_node_data):
    node = Node('test', config_node_data['dict'])
    for key, value in (config_node_data['dict'].items()):
        assert repr(node[key]) == "Node('{}', {})".format(
            key, repr(value))
    with pytest.raises(KeyError):
        node['missing']


@pytest.mark.xfail
def test_confignode_getitem_value(config_node_data):
    node = Node('test', config_node_data['dict'])
    for key, value in (config_node_data['dict'].items()):
        assert node[key].value == value


@pytest.mark.xfail
def test_confignode_getattr(config_node_data):
    node = Node('test', config_node_data['dict'])
    for key, value in (config_node_data['dict'].items()):
        assert repr(getattr(node, key)) == "Node('{}', {})".format(
            key, repr(value))
    getattr(node, 'missing') == 'Node(None, None)'


@pytest.mark.xfail
def test_confignode_getattr_value(config_node_data):
    node = Node('test', config_node_data['dict'])
    for key, value in (config_node_data['dict'].items()):
        assert getattr(node, key).value == value
    assert node.missing.value is None


@pytest.mark.xfail
def test_confignode_nested(config_node_data):
    node = Node('test', config_node_data)
    assert node.dict.dict.int.value == 123
    assert node.dict.dict.str.value == 'other string'
    assert node['dict']['dict']['int'].value == 123
    assert node['dict']['dict']['str'].value == 'other string'


@pytest.mark.xfail
def test_confignode_iterator(config_node_data):
    node = Node('test', config_node_data['dict'])
    assert list(config_node_data['dict'].values()) == [
        subnode.value for subnode in node]
'''
