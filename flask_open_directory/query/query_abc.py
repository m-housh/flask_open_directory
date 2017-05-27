# -*- coding: utf-8 -*-
import abc
import ldap3
from typing import Any, Tuple, Iterable, Union


class QueryABC(metaclass=abc.ABCMeta):
    """This ``abc`` has all the methods that should be implemented for an
    object to be considered a valid ``Query`` subclass.

    All of the methods must be implemented to create a subclass, or to pass
    an ``isinstance`` or ``issubclass`` check.

    """
    @property
    @abc.abstractmethod
    def search_base(self) -> str:  # pragma: no cover
        """Return the ldap serach base dn string for the query.

        """
        pass

    @property
    @abc.abstractmethod
    def search_filter(self) -> str:  # pragma: no cover
        """Return the ldap search filter string for the query.

        """
        pass

    @property
    @abc.abstractmethod
    def connection(self) -> Union[None, ldap3.Connection]:  # pragma: no cover
        """Return the ldap connection for the query.

        """
        pass

    @property
    @abc.abstractmethod
    def ldap_attributes(self) -> Iterable[str]:  # pragma: no cover
        """Return the ldap attributes to return for the query.

        """
        pass

    def first(self, connection: ldap3.Connection=None
              ) -> Any:  # pragma: no cover
        """Searches the ldap connection returning the first entry, if any are
        found or ``None`` if not.

        :param connection:  An optional connection to use for the search.

        """
        pass

    def all(self, connection: ldap3.Connection=None
            ) -> Tuple[Any]:  # pragma: no cover
        """Searches the ldap connection returning tuple of all the entries found.
        Or an empty tuple.

        :param connection:  An optional connection to use for the search.

        """
        pass

    @classmethod
    def __subclasshook__(cls, Cls):
        if cls is QueryABC:
            methods = [
                any('search_base' in dir(Base) for Base in Cls.__mro__),
                any('search_filter' in dir(Base) for Base in Cls.__mro__),
                any('connection' in dir(Base) for Base in Cls.__mro__),
                any('ldap_attributes' in dir(Base) for Base in Cls.__mro__),
                any('all' in dir(Base) for Base in Cls.__mro__),
                any('first' in dir(Base) for Base in Cls.__mro__),
            ]
            if all(methods):
                return True
        return NotImplemented
