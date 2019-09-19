==========================
Python Configraton manager
==========================

Project in early beta. Work in progress!

.. image:: https://travis-ci.org/singulared/conflow.svg?branch=master
    :target: https://travis-ci.org/singulared/conflow
.. image:: https://codecov.io/gh/singulared/conflow/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/singulared/conflow

## Quickstart

```bash
pip install conflow
```

## Usage

```python
from conflow import Config, FromFile, FromEnvironment

LOCAL_SETTINGS = {
    'db': {
        'master': {
            'host': 'localhost',
            'port': 5432,
        },
        'slave': {
            'host': 'localhost',
            'port': 5433,
        }
    },
    'cache': {
        'redis': {
            'sentinel': {
                'host': 'localhost',
                'port': 26379
            }
        }
    }
}

yaml_settings = FromFile(path='settings.yaml')
env_settings = FromEnvironment(prefix='my_app')
config = Config.merge(LOCAL_SETTINGS).merge(yaml_settings).merge(env_settings)
```

## Motivation
If you are tired of making local, test, stage and production profiles in each project, then Conflow is for you.
Conflow allows you to fetch and merge configs from different places - yaml files, environment variables etc.