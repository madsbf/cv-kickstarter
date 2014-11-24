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

      python course_importer.py"


Configuration
=============

To configure the application, it is possible to either add an app.cfg file that contains the relevant configurations (see app.cfg.example for an example configuration file) or environment variables (see cv_kickstarter_config.py for environment variables used).

The app defaults to using MongoDB through localhost unless a MONGO_URL environment variable is given.

Run webserver
=============

To run the web server after the setup, execute:

::

      python webapp.py

or to run with gunicorn, execute:

::

      gunicorn webapp:app --log-file=-


Commmand Line Integration (CV Export)
=====================================

The CV can also be exported in a json format through the CLI by using the command:

::

      jsoncv s123456 secret

where s123456 should be your student id and secret be your password to CampusNet.

Tests
=====

The project uses ``py.test`` for testing, so to run tests, execute:

::

      py.test

The project is also set up with ``tox`` and is tested against python
2.7, 3.4, pypy and pypy3. To run tox locally, type:

::

      python setup.py test

