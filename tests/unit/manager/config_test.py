import pytest

from conflow.manager import Config

DEFAULT_SETTINGS = {
    'db': {
        'master': {
            'host': 'localhost',
            'port': 5432,
        },
        'slave': {
            'host': 'localhost',
            'port': 5433,
        }
    }
}

ENV_SETTINGS = {
    'db': {
        'master': {
            'host': 'env_master_host',
            'port': 5432,
        },
        'slave': {
            'host': 'env_slave_host',
            'port': 5433,
        }
    }
}


@pytest.fixture
def config():
    return Config()


def test_config_first_merge(config):
    config.merge(DEFAULT_SETTINGS)
    assert config.layer is not None


def test_config_merge(config):
    config = config.merge(DEFAULT_SETTINGS)
    assert config.layer.tree().db.master.host == 'localhost'
    config = config.merge(ENV_SETTINGS)
    assert config.layer.tree().db.master.host == 'env_master_host'


def test_config_get_attr(config):
    config = config.merge(DEFAULT_SETTINGS)
    assert config.db.master.host == 'localhost'


def test_config_get_item(config):
    config = config.merge(DEFAULT_SETTINGS)
    assert config['db']['master']['host'] == 'localhost'
