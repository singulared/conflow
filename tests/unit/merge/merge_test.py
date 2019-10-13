from conflow.merge import merge_factory
from conflow.node import Node, NodeList, NodeMap
from conflow.policy import MergePolicy


def test_merge_node_node():
    base = Node('base', 'node_A')
    other = Node('other', 'node_B')
    assert merge_factory(base, other, MergePolicy.OVERRIDE) == other


def test_merge_nodelist_nodelist_override():
    base = NodeList('base', [1])
    other = NodeList('other', [2])
    assert merge_factory(base, other, MergePolicy.OVERRIDE) == other


def test_merge_nodelist_nodelist_extend():
    base = NodeList('base', [1])
    other = NodeList('other', [2])
    expected = NodeList('base', [1, 2])
    assert merge_factory(base, other, MergePolicy.EXTEND) == expected


def test_merge_nodemap_nodemap_override():
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
    result = merge_factory(base, other, MergePolicy.EXTEND)
    assert result.db.master.host == 'other'


def test_merge_nodemap_nodemap_extend():
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
    result = merge_factory(base, other, MergePolicy.EXTEND)
    assert 'master' in result
    assert 'slave' in result


def test_merge_nodemap_nodemap_empty():
    base = NodeMap('base', {})
    other = NodeMap('other', {})
    expected = NodeMap('expected', {})
    assert merge_factory(base, other, MergePolicy.EXTEND) == expected
