import conflow
import pytest
import os

from conflow import FromEnv
from conflow.froms.environment import try_str_int

ENV_SETTINGS = {
    'APP_DB__MASTER__HOST': 'localhost',
    'APP_DB__MASTER__PORT' : '5432',
}

DICT_REPRESENTATION = {
        'db': {
            'master': {
                'host': 'localhost',
                'port': 5432
            }
        }
    }


@pytest.fixture
def env_fixture():
    for key, value in ENV_SETTINGS.items():
        os.environ[key] = value


def test_from_environment_exists():
    assert hasattr(conflow, 'FromEnv')


def test_from_environment_correct_loads(env_fixture):
    env = FromEnv('APP')
    selected = env.load_by_prefix()
    assert len(selected) == 2
    assert 'APP_DB__MASTER__HOST' in selected
    assert 'APP_DB__MASTER__PORT' in selected


def test_from_environment_correct_adds_pairs():
    env = FromEnv('APP')
    env.add_pair('APP_DB__MASTER__HOST', 'localhost')
    env.add_pair('APP_DB__MASTER__PORT', '5432')
    assert env.map == DICT_REPRESENTATION


def test_from_environment_correct_parses(env_fixture):
    env = FromEnv('APP')
    env.parse()
    assert env.map == DICT_REPRESENTATION


def test_from_environment_try_str_int():
    assert try_str_int('5432') == 5432
    assert try_str_int(5432) == 5432
    assert try_str_int('abc') == 'abc'
    assert try_str_int('76.2') == '76.2'


def test_from_environment_get_item(env_fixture):
    env = FromEnv('APP')
    assert env['db'] == DICT_REPRESENTATION['db']
    assert env['db']['master'] == DICT_REPRESENTATION['db']['master']
