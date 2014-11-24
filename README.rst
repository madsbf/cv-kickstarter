CVKickstarter
=============

Data Mining using Python project repository

Setup
=====

To install required modules, simply type:

::

      python setup.py install

For optimization reasons, the course information is fetched from a MongoDB database. In order to import courses into MongoDB from the xml, run the command:

::

      python -c "import course_importer; course_importer.import_courses()"


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

