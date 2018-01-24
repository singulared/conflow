from setuptools.command.test import test as TestCommand
from setuptools import setup
import sys


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ''

    def run_tests(self):
        import shlex
        # import here, cause outside the eggs aren't loaded
        import pytest
        sys.dont_write_bytecode = True
        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


install_requires = [
    'PyYAML==3.12'
]

tests_require = [
    'pytest==3.3.2',
    'pytest-cov==2.5.1',
    'pytest-sugar==0.9.0',
]

lint_require = [
    'flake8==3.5.0',
    'flake8-html==0.4.0',
]

static_require = [
    'mypy==0.560',
    'lxml==4.1.1',
]

setup_requires = [
    'setuptools-scm==1.15.6'
]

dev_require = [
    'ipdb==0.10.3'
]

extras_require = {
    'test': tests_require,
    'dev': dev_require,
    'lint': lint_require,
    'static': static_require,
    'ci': static_require + lint_require + tests_require,
}

cmdclass = {
    'test': PyTest,
}


setup(
    use_scm_version=True,
    cmdclass=cmdclass,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require=extras_require,
    setup_requires=setup_requires
)
