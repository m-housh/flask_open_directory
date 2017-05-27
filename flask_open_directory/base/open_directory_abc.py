# -*- coding: utf-8 -*-
import abc
from typing import Union
from contextlib import contextmanager
import ldap3


ConnectionCtx = Union[None, ldap3.Connection]


class OpenDirectoryABC(metaclass=abc.ABCMeta):
    """This ``abc`` has all the methods that should be implemented for an
    object to be considered a valid ``OpenDirectory`` subclass.


    All of the methods must be implemented to create a subclass, or to pass
    an ``isinstance`` or ``issubclass`` check.


    """
    @property
    @abc.abstractmethod
    def server_url(self) -> str:  # pragma: no cover
        """Return the ldap server url.  Used for the ldap connection.

        """
        pass

    @property
    @abc.abstractmethod
    def base_dn(self) -> str:  # pragma: no cover
        """Return the base ldap domain.  Used to build ldap queries.

        """
        pass

    @property
    @abc.abstractmethod
    def connection(self) -> Union[ldap3.Connection, None]:  # pragma: no cover
        """An :class:`ldap3.Connection` used for queries.  This should only
        return a connection if there is a flask application running with the
        connection stored on it.

        """
        pass

    @contextmanager
    @abc.abstractmethod
    def connection_ctx(self) -> ConnectionCtx:  # pragma: no cover
        """A context manager to yield an :class:`ldap3.Connection`, this should
        try to create a connection regardless of if a flask application is
        running.

        """
        pass

    @classmethod
    def __subclasshook__(cls, Cls):
        if cls is OpenDirectoryABC:
            methods = [
                any('server_url' in dir(B) for B in Cls.__mro__),
                any('base_dn' in dir(B) for B in Cls.__mro__),
                any('connection' in dir(B) for B in Cls.__mro__),
                any('connection_ctx' in dir(B) for B in Cls.__mro__),
            ]
            if all(methods):
                return True
        return NotImplemented
