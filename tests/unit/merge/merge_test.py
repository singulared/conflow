from conflow.merge import merge_factory
from conflow.node import Node, NodeList, NodeMap


def test_merge_node_node(default_config):
    base = Node('base', 'node_A')
    other = Node('other', 'node_B')
    assert merge_factory(base, other, default_config) == other


def test_merge_node_nodelist(default_config):
    base = Node('base', 'node_A')
    other = NodeList('other', [2])
    assert merge_factory(base, other, default_config) == other


def test_merge_node_nodemap(default_config):
    base = Node('base', 'node_A')
    other = NodeMap('other', {
        'db': {
            'master': {
                'host': 'other'
            }
        }
    })
    assert merge_factory(base, other, default_config) == other


def test_merge_nodelist_node(default_config):
    base = NodeList('other', [2])
    other = Node('base', 'node_A')
    assert merge_factory(base, other, default_config) == other


def test_merge_nodelist_nodelist_override(default_config):
    base = NodeList('base', [1])
    other = NodeList('other', [2])
    assert merge_factory(base, other, default_config) == other


def test_merge_nodelist_nodelist_extend(extend_list_config):
    base = NodeList('base', [1])
    other = NodeList('other', [2])
    expected = NodeList('base', [1, 2])
    assert merge_factory(base, other, extend_list_config) == expected


def test_merge_nodelist_nodemap(default_config):
    base = NodeList('base', [1])
    other = NodeMap('base', {
        'db': {
            'master': {
                'host': 'base'
            }
        }
    })
    assert merge_factory(base, other, default_config) == other


def test_merge_nodemap_node(default_config):
    base = NodeMap('base', {
        'db': {
            'master': {
                'host': 'base'
            }
        }
    })
    other = Node('base', 'node_A')
    assert merge_factory(base, other, default_config) == other


def test_merge_nodemap_nodelist(default_config):
    base = NodeMap('base', {
        'db': {
            'master': {
                'host': 'base'
            }
        }
    })
    other = NodeList('base', [1])
    assert merge_factory(base, other, default_config) == other


def test_merge_nodemap_nodemap_override(default_config):
    base = NodeMap('base', {
        'db': {
            'master': {
                'host': 'base'
            }
        }
    })
    other = NodeMap('other', {
        'db': {
            'master': {
                'host': 'other'
            }
        }
    })
    result = merge_factory(base, other, default_config)
    assert result.db.master.host == 'other'


def test_merge_nodemap_nodemap_extend(default_config):
    base = NodeMap('base', {
        'master': {
            'host': 'master'
        }
    })
    other = NodeMap('other', {
        'slave': {
            'host': 'slave'
        }
    })
    result = merge_factory(base, other, default_config)
    assert 'master' in result
    assert 'slave' in result


def test_merge_nodemap_nodemap_empty(default_config):
    base = NodeMap('base', {})
    other = NodeMap('other', {})
    expected = NodeMap('expected', {})
    assert merge_factory(base, other, default_config) == expected
