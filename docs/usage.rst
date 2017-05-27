=====
Usage
=====

.. module:: flask_open_directory

To use Flask-OpenDirectory in a project::

    from flask import Flask
    from flask_open_directory import OpenDirectory


    app = Flask(__name__)
    open_directory = OpenDirectory(app)


Or if using application factories::

    from flask_open_directory import OpenDirectory

    open_directory = OpenDirectory()
    open_directory.init_app(app)


Configuration
-------------

Configuration is done along with your normal ``Flask`` configuration or through
environment variables.


The following variables are used with Flask-OpenDirectory::

    OPEN_DIRECTORY_SERVER = 'example.com'  # default: 'localhost'

    # this is optional, espically for this usecase, as we will parse the
    # server url 'example.com' to this same base dn, if not supplied.  
    # However, if your base dn does not match your server url, then it
    # can be useful to supply your own.
    OPEN_DIRECTORY_BASE_DN = 'dc=example,dc=com'


    app = Flask(__name__)
    app.config['OPEN_DIRECTORY_SERVER'] = OPEN_DIRECTORY_SERVER
    app.config['OPEN_DIRECTORY_BASE_DN'] = OPEN_DIRECTORY_BASE_DN

    open_directory = OpenDirectory(app)


If the above variables are not with the application configuration, then we
will look for environment variables (using the same names) as above.


Route Authorization
-------------------

There are several built-in decorators that can be used to mark a route for
authorization.

Example Application:
~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/route_authorization.py
    :language: python

Start the application:
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash
    
    $ python route_authorization.py
        

Test with curl:
~~~~~~~~~~~~~~~

    Use the ``--basic`` authentication flag for curl to set an ``Authorization``
    header.  So that our methods will have access to the username the request is
    for.

.. code-block:: bash

    $ curl --basic -u office_user http://localhost:5000/office-or-admins


.. _custom_decorators:

Custom Authorization Decorators
-------------------------------

Flask-OpenDirectory includes a :func:`pass_context` helper when creating your own 
custom authorization decorators.  This will pass a :class:`DecoratorContext`,
which is a specialized :class:`dict` like object as the first argument to your 
decorator that gives you access to the :class:`OpenDirectory` registered with the 
current application, as well as the ``username`` from the 
``request.authorization`` header.

Basic Example:
~~~~~~~~~~~~~~

.. literalinclude:: ../examples/custom_decorator.py
    :language: python


Start the Application:
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash
    
    $ python custom_decorator.py

Test with curl:
~~~~~~~~~~~~~~~

    Use the ``--basic`` authentication flag for curl to set an ``Authorization``
    header.  So that our methods will have access to the username the request is
    for.  The password used doesn't really matter here, since there is no 
    authentication middleware present.

.. code-block:: bash

    $ curl --basic -u george http://localhost:5000/george


The above is a pretty silly and simple example, most likely you are going to
want to do more than compare the username.  Odds are you are going to need to
query the ``OpenDirectory``, using the :meth:`OpenDirectory.query`.  The
query syntax is very similar to the popular ``SQLAlchemy`` package syntax.


Below is an example showing the internals of the ``requires_group`` decorator.

Advanced Example
~~~~~~~~~~~~~~~~

.. code-block:: python

    from flask_open_directory import Group, pass_context

    def requires_group(group_name):
        """Decorator to ensure the user is a member of the specified group.

        """
        def inner(fn):

            @wraps(fn)
            @pass_context
            def decorator(ctx, *args, **kwargs):
                open_directory, username = ctx.open_directory, ctx.username
                
                # query the open_directory connection for the specified group.
                group = open_directory.query(Group)\
                    .filter(group_name=group_name)\
                    .first()

                # check that the user is a member of the group
                if group.has_user(username):
                    return fn(*args, **kwargs)
                return abort(401)

            return decorator

        return inner


Custom Model Creation
---------------------

If you need to query for models other than what is already created by this 
package, then you will need to create a custom model to map the
``OpenDirectory`` attributes to your python object.  The trickiest part on
creating custom models, is determining the ldap entry key to use to map to your
python object.

Below are some useful resources/commands to look into, to help determine which
ldap keys to use:

* (On macOS) /etc/openldap/schema :  Contains the ldap schema(s) used for macOS
* ``$ man dscl``  :  apple's directory utility command line interface
* ``$ man ldapsearch``  :  ldap search utility syntax is tough to get used to,
  but tends to be the best resource (for me) to find attribute names.

Example:

    .. literalinclude:: ../examples/custom_model.py
        :language: python

