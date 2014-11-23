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


class NLTKDataDownloader(object):
    @classmethod
    def download(_class):
        import nltk
        nltk.download(
            ['maxent_treebank_pos_tagger', 'punkt'],
            download_dir='./nltk_data'
        )


class ToxTestCommand(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        NLTKDataDownloader.download()
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
        'requests',
        'Flask',
        'flask-negotiate',
        'flask-sslify',
        'gunicorn',
        'Werkzeug',
        'nltk',
        'numpy'
        'Flask-PyMongo'
    ],
    tests_require=['tox'],
    url='http://github.com/MadsFrandsen/PyCampus',
    cmdclass={'test': ToxTestCommand}
)
