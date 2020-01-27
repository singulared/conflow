import conflow
import pytest
import os

from conflow import from_env
from conflow.froms.environment import try_str_int, load_by_prefix, add_pair

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
    assert hasattr(conflow, 'from_env')


def test_from_environment_correct_loads(env_fixture):
    selected = load_by_prefix('APP')
    assert len(selected) == 2
    assert 'DB__MASTER__HOST' in selected
    assert 'DB__MASTER__PORT' in selected


def test_from_environment_correct_adds_pairs():
    env_map = {}
    add_pair(env_map, 'DB__MASTER__HOST', 'localhost')
    add_pair(env_map, 'DB__MASTER__PORT', '5432')
    assert env_map == DICT_REPRESENTATION


def test_from_environment_correct_parses(env_fixture):
    env = from_env('APP')
    assert env == DICT_REPRESENTATION


def test_from_environment_try_str_int():
    assert try_str_int('5432') == 5432
    assert try_str_int(5432) == 5432
    assert try_str_int('abc') == 'abc'
    assert try_str_int('76.2') == '76.2'


def test_from_environment_get_item(env_fixture):
    env = from_env('APP')
    assert env['db'] == DICT_REPRESENTATION['db']
    assert env['db']['master'] == DICT_REPRESENTATION['db']['master']
