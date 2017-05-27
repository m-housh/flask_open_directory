# -*- coding: utf-8 -*-
import abc
from typing import Dict, Union, Tuple, Any
import ldap3


class ModelABC(metaclass=abc.ABCMeta):
    """An abstract class with some default implementations for a model, which
    maps the ``OpenDirectory (ldap attributes)`` to a python object.

    Any of the methods that have a default implementation can be accessed on
    a derived subclass via the ``super`` mechanism.

    """
    _query_cn = None

    @classmethod
    @abc.abstractmethod
    def ldap_attribute_map(cls) -> Dict[str, str]:  # pragma: no cover
        """Return a mapping of <model attribute: ldap key> values.

        This does not have a default implementation, and must be implemented
        on the subclass.

        """
        pass

    @classmethod
    def ldap_keys(cls) -> Tuple[str]:
        """Return all the ldap keys

        This default implementation returns the ``values`` from the
        :meth:`ldap_attribute_map`.

        You can use the default implementation from the ``super`` mechanism in
        your subclass.

        """
        return tuple(cls.ldap_attribute_map().values())

    @classmethod
    def attribute_name_for(cls, ldap_key: str) -> Union[None, str]:
        """Retrieve the python model object's attribute name for a given ldap
        entry key.

        This default implementation checks the :meth:`ldap_attribute_map`,
        returning, ``key`` for the ``value`` in the mapping, or ``None`` if
        not found.

        You can use the default implementation from the ``super`` mechanism in
        your subclass.

        :param ldap_key:  The ldap entry key.

        """
        for key, value in cls.ldap_attribute_map().items():
            if str(value) == str(ldap_key):
                return key

    @classmethod
    def query_cn(cls) -> str:
        """Return the query cn to be used in queries. This value will get
        added to the ``base_dn`` as 'cn=<this value>,<base_dn>' for queries.

        The default implementation returns the lower case version of the class
        name and appends an 's'.

        You can use the default implementation from the ``super`` mechanism in
        your subclass.

        Example::

            # given a base dn of 'dc=example,dc=com'
            >>> class User(ModelABC): pass
            >>> open_directory = OpenDirectory()
            >>> query = Query(open_directory=open_directory, model=User)
            >>> query.search_base
            'cn=users,dc=example,dc=com'

        """
        return cls._query_cn or cls.__name__.lower() + 's'

    @classmethod
    def from_entry(cls, entry: ldap3.Entry) -> Any:
        """Return an instance of the class from an :class:`ldap3.Entry`

        The default implementation requires that a subclass accepts ``kwargs``
        for all attributes in it's ``__init__`` method.

        :param entry:  An :class:`ldap3.Entry` to convert to this python model.

        :rtype:  An instance of the python model.

        """
        return cls(**entry.entry_attributes_as_dict)

    @classmethod
    def __subclasshook__(cls, Cls):
        if cls is ModelABC:
            methods = [
                any('ldap_attribute_map' in dir(B) for B in Cls.__mro__),
                any('attribute_name_for' in dir(B) for B in Cls.__mro__),
                any('query_cn' in dir(B) for B in Cls.__mro__),
                any('from_entry' in dir(B) for B in Cls.__mro__),
                any('ldap_keys' in dir(B) for B in Cls.__mro__),
            ]
            if all(methods):
                return True
        return NotImplemented  # pragma: no cover
