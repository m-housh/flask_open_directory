===============================
Flask-OpenDirectory
===============================


.. image:: https://img.shields.io/pypi/v/flask_open_directory.svg
        :target: https://pypi.python.org/pypi/flask_open_directory

.. image:: https://readthedocs.org/projects/flask-open-directory/badge/?version=latest
        :target: https://flask-open-directory.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

MacOS OpenDirectory Authorization Middleware for Flask

This package is tailored to my use-case, where my Authentication is from
MacOS Server, which authenticates a user, however I need to have specific 
Flask routes, that only allow users of certain OpenDirectory groups.  

So that's why I call this an Authorization Middleware, however it could be a
base for someone who would like to implement a full authorization layer.

This package utilizes an ``LDAP`` connection to query the ``OpenDirectory``, it
is setup to only do ``read`` operations with the connection.


* Free software: MIT license
* Documentation: https://flask-open-directory.readthedocs.io.


Features
--------

* Flask extension to incorporate macOS OpenDirectory authorization into your
  Flask application.

Credits
---------

This package utilizes the following packages as dependencies.

* `Flask <http://flask.pocoo.org>`_ licensed under the 
  `BSD License <http://flask.pocoo.org/docs/0.12/license/>`_

* `Ldap3 <http://ldap3.readthedocs.io>`_ licensed under the 
  `LGPL3 License <http://www.gnu.org/licenses/lgpl-3.0.html>`_

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

