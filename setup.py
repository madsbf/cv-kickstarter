import os
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand

__name__ = 'CVKickstarter'
__version__ = '0.1.0'
__author__ = 'Mads Frandsen & Anders Nielsen'
__author_email__ = 's082972@student.dtu.dk & aemilnielsen@gmail.com'
__doc__ = """
CVKickstarter is a web app that is able to analyse your DTU information
and provide you with a prefilled CV with your education information, courses
you've passed, the performance of your study, the skills you've gained and
job suggestions based on your best skills.
"""


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
    description=__doc__,
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
        'Flask-PyMongo>=0.3.0,<0.4.0'
    ],
    tests_require=['tox'],
    url='http://github.com/MadsFrandsen/PyCampus',
    cmdclass={'test': ToxTestCommand}
)
