import pytest
import mock

import conflow
from conflow import FromYaml


@pytest.fixture
def yaml_fixture():
    yaml = """
      db:
        master:
          host: localhost
          port: 5432
    """
    return yaml


def test_from_yaml_exists():
    assert hasattr(conflow, 'FromYaml')


def test_from_yaml_correct_parses(yaml_fixture):
    mocked_open = mock.mock_open(read_data=yaml_fixture)
    with mock.patch('conflow.froms.yml.open', mocked_open):
        yml = FromYaml('file.yaml')
        assert yml['db']['master']['host'] == 'localhost'
        assert yml['db']['master']['port'] == 5432
