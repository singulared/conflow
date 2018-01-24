import pytest
from conflow.node import ConfigNode


def test_confignode(config_node_data):
    node = ConfigNode('test', config_node_data['dict'])
    assert node.dict
    assert repr(node) == "ConfigNode('test', {})".format(
        config_node_data['dict'])


def test_confignode_in(config_node_data):
    node = ConfigNode('test', config_node_data['dict'])
    assert 'int' in node
    assert 'list' in node
    assert 'none' in node
    assert 'missing' not in node


def test_confignode_repr(config_node_data):
    node = ConfigNode('test', config_node_data)
    assert repr(node) == 'ConfigNode(\'test\', {})'.format(config_node_data)


def test_confignode_getitem(config_node_data):
    node = ConfigNode('test', config_node_data['dict'])
    for key, value in (config_node_data['dict'].items()):
        assert repr(node[key]) == "ConfigNode('{}', {})".format(
            key, repr(value))
    with pytest.raises(KeyError):
        node['missing']


def test_confignode_getitem_value(config_node_data):
    node = ConfigNode('test', config_node_data['dict'])
    for key, value in (config_node_data['dict'].items()):
        assert node[key].value == value


def test_confignode_getattr(config_node_data):
    node = ConfigNode('test', config_node_data['dict'])
    for key, value in (config_node_data['dict'].items()):
        assert repr(getattr(node, key)) == "ConfigNode('{}', {})".format(
            key, repr(value))
    getattr(node, 'missing') == 'ConfigNode(None, None)'


def test_confignode_getattr_value(config_node_data):
    node = ConfigNode('test', config_node_data['dict'])
    for key, value in (config_node_data['dict'].items()):
        assert getattr(node, key).value == value
    assert node.missing.value is None


def test_confignode_nested(config_node_data):
    node = ConfigNode('test', config_node_data)
    assert node.dict.dict.int.value == 123
    assert node.dict.dict.str.value == 'other string'
    assert node['dict']['dict']['int'].value == 123
    assert node['dict']['dict']['str'].value == 'other string'


def test_confignode_iterator(config_node_data):
    node = ConfigNode('test', config_node_data['dict'])
    assert list(config_node_data['dict'].values()) == [
        subnode.value for subnode in node]
