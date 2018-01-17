from conflow.node import ConfigNode


def test_confignode(config_node_data):
    node = ConfigNode('dict', config_node_data['dict'])
    assert node.dict
