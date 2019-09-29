from conflow.manager import Config

DEFAULT = {
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


OVERRIDE = {
    'db': {
        'master': {
            'host': 'overridden_localhost',
            'timeout': 1000,
        }
    },
    'cache': {
        'redis': {
            'master': {
                'host': 'overridden_localhost',
                'timeout': 1000,
            }
        }
    }
}


def test_config_init():
    config = Config(DEFAULT).merge(OVERRIDE)
    assert len(config._Config__layers) == 2
    config = Config()
    assert len(config._Config__layers) == 0


def test_config_merged():
    config = Config(DEFAULT).merge(OVERRIDE)
    config.compile()
    self_id = id(config)
    config_value = config._Config__map_path_node[(self_id, 'db', 'master', 'host')]
    assert len(config_value) == 2
    assert config_value.popleft() == OVERRIDE['db']['master']['host']


def test_config_compile():
    config = Config(DEFAULT).merge(OVERRIDE)
    config.compile()
    assert config.tree.db.master.host() == OVERRIDE['db']['master']['host']
    assert len(config.tree()) == 2
    assert len(config.tree.db()) == 1
    assert len(config.tree.db.master()) == 5
