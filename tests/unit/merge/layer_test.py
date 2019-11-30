from conflow.layer import Layer
from conflow.node import node_factory


def test_layer_tree(default_config):
    node_data = {'a': 1}
    layer = Layer(default_config, node_data, 'test')
    node = node_factory('test', node_data)
    assert layer.tree() == node


def test_layer_merge(default_config):
    base_layer = Layer(default_config, {'a': 1}, 'test')
    other_layer = Layer(default_config, {'a': 2}, 'test')
    base_layer.merge(other_layer)
    assert base_layer.tree().a == 2
