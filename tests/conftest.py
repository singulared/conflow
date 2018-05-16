import pytest


@pytest.fixture
def config_node_data():
    return {
        'dict': {
            'int': 123,
            'str': 'string',
            'float': 123.321,
            'list': [1, 2, '3'],
            'nested_list': [[3, 2, 1], [1, 2, 3]],
            'nested_map': {'list': [1, 2, 3], 'map': {
                'str': 'string', 'int': 321}},
            'set': {1, 2, '3'},
            'dict': {'int': 123, 'str': 'other string'},
            'none': None
        }
    }
