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


def req_file(filename):
    with open(filename) as f:
        content = f.readlines()
    return [x.strip() for x in content]


install_requires = [
    req_file('requirements.txt')
]

tests_require = [
    req_file('requirements-tests.txt')
]

lint_require = [
    req_file('requirements-lint.txt')
]

static_require = [
    req_file('requirements-static.txt')
]

setup_requires = [
    'setuptools-scm==1.15.6'
]

dev_require = [
    req_file('requirements-dev.txt')
]

extras_require = {
    'test': tests_require,
    'dev': dev_require + tests_require,
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
