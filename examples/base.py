import os
from conflow import Config, from_env, from_yaml
from typing import Dict

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

config = Config().merge(DEFAULT_SETTINGS)
assert config.db.master.host() == 'localhost'

os.environ['APP_DB__MASTER__HOST'] = 'remote_host'
env_settings: Dict = from_env('APP')

config = Config().merge(DEFAULT_SETTINGS).merge(env_settings)
assert config.db.master.host() == 'remote_host'

develop_settings: Dict = from_yaml('config/develop.yaml', required=False)
config = Config().merge(
    DEFAULT_SETTINGS
).merge(env_settings).merge(develop_settings)
assert config.db.master.host() == 'develop'
