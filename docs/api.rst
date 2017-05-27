===
API
===

The public interface for ``Flask-OpenDirectory``.

.. module:: flask_open_directory

OpenDirectory
-------------

.. autoclass:: OpenDirectory
    :members:
    :show-inheritance:
    :inherited-members:
    :noindex:

Decorators
----------

This package contains the following decorators/ decorator helpers.

.. autofunction:: requires_group
    :noindex:

.. autofunction:: requires_any_group
    :noindex:

.. autofunction:: requires_all_groups
    :noindex:

.. autofunction:: pass_context
    :noindex:

Models
------

The following models are included as part of the package, however a user is
welcome to create there own as well.

.. autoclass:: User
    :members:
    :noindex:
    :show-inheritance:

.. autoclass:: Group
    :members:
    :noindex:
    :show-inheritance:


Query
-----

The following class is not often used directly, it is typically easier to use
the :meth:`OpenDirectory.query`, to get a query that is already setup.

.. autoclass:: Query
    :members:
    :noindex:
    :show-inheritance:
    :inherited-members:

Utilities
---------

.. module:: flask_open_directory.utils

This package includes the following utility methods.  These are not importable
from the main entrypoint, these need to be imported directly from
``flask_open_directory.utils`` module.


.. autofunction:: base_dn_from_url
    :noindex:

.. autofunction:: username_from_request
    :noindex:


Base Classes and Helper Classes
-------------------------------

.. module:: flask_open_directory

This package includes the following base classes, which are good place to start
if trying to implement your own sub-classes.

.. autoclass:: BaseOpenDirectory
    :members:
    :noindex:
    :show-inheritance:
    :inherited-members:

.. autoclass:: BaseModel
    :members:
    :noindex:
    :show-inheritance:
    :inherited-members:

.. autoclass:: BaseQuery
    :members:
    :noindex:
    :show-inheritance:
    :inherited-members:

.. autoclass:: DecoratorContext
    :members:
    :noindex:
    :show-inheritance:

.. autoclass:: Attribute
    :members:
    :noindex:
    :show-inheritance:
    :inherited-members:


Abstract Classes
----------------

This package provides the following abstract classes, that can be used to test
if an object implements the correct interface.

.. autoclass:: OpenDirectoryABC
    :members:
    :noindex:
    :show-inheritance:
    :inherited-members:

.. autoclass:: ModelABC
    :members:
    :noindex:
    :show-inheritance:
    :inherited-members:

.. autoclass:: QueryABC
    :members:
    :noindex:
    :show-inheritance:
    :inherited-members:

