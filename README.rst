CVKickstarter
=============

Data Mining using Python project repository

Setup
=====

To install required modules, simply type:

::

      python setup.py install

Run webserver
=============

To run the web server after the setup, execute:

::

      python webapp.py

or to run with gunicorn, execute:

::

      gunicorn webapp:app --log-file=-

Tests
=====

The project uses ``py.test`` for testing, so to run tests, execute:

::

      py.test

The project is also set up with ``tox`` and is tested against python
2.7, 3.4, pypy and pypy3. To run tox locally, type:

::

      python setup.py test

