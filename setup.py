import os
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

import cv_kickstarter


class ToxTestCommand(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        sys.exit(os.system('tox'))

setup(
    name=cv_kickstarter.__name__,
    version=cv_kickstarter.__version__,
    author=cv_kickstarter.__author__,
    license='MIT',
    description=cv_kickstarter.__doc__,
    packages=find_packages(),
    keywords='cv kickstarter dtu student',
    long_description=open('README.rst').read(),
    install_requires=[
        'requests>=2.4.3,<2.5.0',
        'Flask>=0.10.1,<0.11.0',
        'flask-negotiate>=0.1.0,<0.2.0',
        'flask-sslify>=0.1.4,<0.2.0',
        'gunicorn>=19.1.1,<19.2.0',
        'Werkzeug>=0.9.6,<1.0.0',
        'nltk>=3.0.0,<3.1.0',
        'numpy>=1.9.1,<2.0.0',
        'beautifulsoup4==4.3.1',
        'lxml==3.4.1',
        'PyMongo>=2.7.0,<2.8.0',
        'docopt>=0.6.0,<0.7.0',
        'opbeat>=1.3.2,<1.4.0',
        'blinker>=1.3,<1.4'
    ],
    tests_require=['tox'],
    scripts=['bin/jsoncv'],
    url='http://github.com/MadsFrandsen/PyCampus',
    cmdclass={'test': ToxTestCommand}
)
