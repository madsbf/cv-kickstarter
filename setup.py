import os
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand

__name__ = 'CVKickstarter'
__version__ = '0.1.0'
__author__ = 'Mads Frandsen & Anders Nielsen'


class ToxTestCommand(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        sys.exit(os.system('tox'))

setup(
    name=__name__,
    version=__version__,
    author=__author__,
    license='MIT',
    keywords='cv kickstarter dtu student',
    install_requires=[
        'requests',
        'flask',
        'flask-negotiate',
        'flask-sslify',
        'gunicorn'
    ],
    tests_require=['tox'],
    url='http://github.com/MadsFrandsen/PyCampus',
    cmdclass={'test': ToxTestCommand}
)
