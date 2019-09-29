import pytest
from conflow.layer import flatten_tree, path_from
from conflow.node import NodeMap

TREE_BASE = {
    'db': {
        'master': {
            'host': 'localhost',
            'port': 5432,
            'user': 'local',
            'password': 'local',
        }
    },
    'cache': {
        'redis': {
            'master': {
                'host': 'localhost',
                'port': 6379,
            }
        }
    }
}

PATH = {
    'db': {
        'master': {
            'host': {
                'base': None
            },
        }
    }
}

LIST_PATH = {
    'db': [
        {
            'master': None
        },
        {
            'slave': None
        },
    ]
}


def test_flatten_tree_result_has_correct_len():
    tree = NodeMap('test', TREE_BASE)
    leafs = list(flatten_tree(None, tree))
    assert len(leafs) == 6


def test_flatten_tree_result_has_correct_path_with_map():
    tree = NodeMap('test', PATH)
    first_leaf = list(flatten_tree(None, tree))[0]
    assert first_leaf[0] == ('test', 'db', 'master', 'host', 'base')


def test_flatten_tree_result_has_correct_path_with_list():
    tree = NodeMap('test', LIST_PATH)
    first_leaf = list(flatten_tree(None, tree))[0]
    assert first_leaf[0] == ('test', 'db')


@pytest.mark.parametrize('path, key, expected', [
    (None, 'test', ('test',)),
    (('test', 'db', 'master'), 'host', ('test', 'db', 'master', 'host'))
])
def test_path_from(path, key, expected):
    path_with_key = path_from(path, key)
    assert path_with_key == expected
