import pytest


@pytest.fixture
def config_node_data():
    return {
        'dict': {
            'int': 123,
            'str': 'string',
            'float': 123.321,
            'list': [1, 2, '3'],
            'set': {1, 2, '3'},
            'dict': {'int': 123, 'str': 'other string'},
            'none': None
        }
    }
