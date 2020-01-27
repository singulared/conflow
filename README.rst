=======
Conflow
=======

.. image:: https://travis-ci.org/singulared/conflow.svg?branch=master
    :target: https://travis-ci.org/singulared/conflow
.. image:: https://codecov.io/gh/singulared/conflow/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/singulared/conflow

Project in early beta. Work in progress!

Conflow organizes layered configurations for Python applications.
Conflow allows you to use default settings and extend or override it
via merging settings from different sources:
- Python dictionaries
- Files: yaml, json, ini
- Environment variables

Quickstart
==========

.. code-block:: bash

  pip install conflow

Usage
=====

.. code-block:: python

  import os
  from conflow import Config, from_env

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
  env_settings = from_env('APP')

  config = Config().merge(DEFAULT_SETTINGS).merge(env_settings)
  assert config.db.master.host() == 'remote_host'

Motivation
==========
If you are tired of making local, test, stage and production profiles in each project, then Conflow is for you.
Conflow allows you to fetch and merge configs from different places - yaml files, environment variables etc.
