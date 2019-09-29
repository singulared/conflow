============================
Python Configuration manager
============================

.. image:: https://travis-ci.org/singulared/conflow.svg?branch=master
    :target: https://travis-ci.org/singulared/conflow
.. image:: https://codecov.io/gh/singulared/conflow/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/singulared/conflow

Project in early beta. Work in progress!

Quickstart
==========

.. code-block:: bash

  pip install conflow

Usage
=====

.. code-block:: python

  from conflow import Config, FromFile, FromEnvironment

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

  stage_settings = FromFile(path='stage.yaml')
  env_settings = FromEnvironment(prefix='my_app')
  config = Config(DEFAULT_SETTINGS).merge(stage_settings).merge(env_settings)

Motivation
==========
If you are tired of making local, test, stage and production profiles in each project, then Conflow is for you.
Conflow allows you to fetch and merge configs from different places - yaml files, environment variables etc.
