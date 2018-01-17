import pytest


@pytest.fixture
def config_node_data():
    return {
        'dict': {
            'int': 123,
            'float': 123.321,
            'list': [1, 2, '3'],
            'none': None
        }
    }
