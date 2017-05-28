# -*- coding: utf-8 -*-
from typing import Union, Iterable, Any, Tuple
from contextlib import contextmanager
import ldap3

from .query_abc import QueryABC
from ..model import ModelABC
from ..base import OpenDirectoryABC
from .._compat import ContextManager


ConnectionCtx = ContextManager[Union[None, ldap3.Connection]]


def _quote_if_str(val):
    """Helper to quote a value if it's a string.

    """
    if isinstance(val, str):
        return "'{}'".format(val)
    return val


class BaseQuery(QueryABC):
    """Implementation of :class:`QueryABC` abstract class.  This is used to
    search an ldap connection and convert the entries into a :class:`ModelABC`
    subclass.

    This also adds a helpful context manager :meth:`BaseQuery.connection_ctx`,
    which is helpful if you do not have a flask application running, it will
    try to create a connection with the ``open_directory`` set on the instance
    for the search.

    """
    # used if no search filter is set on an instance.
    _default_search_filter = '(objectClass=*)'

    def __init__(self, open_directory: Any=None,
                 model: Any=None,
                 search_base: str=None,
                 search_filter: str=None,
                 connection: ldap3.Connection=None,
                 ldap_attributes: Iterable[str]=None
                 ) -> None:

        self.search_base = search_base
        self.search_filter = search_filter
        self.connection = connection
        self.ldap_attributes = ldap_attributes
        self.model = model
        self.open_directory = open_directory

    @property
    def model(self) -> Any:
        """A :class:`ModelABC` subclass used for search criterea and
        to in converting returned entries into the desired model.

        The attribute can be set with either a class or an instance of a class,
        but we always store a reference to the class.

        """
        return getattr(self, '_model', None)

    @model.setter
    def model(self, value) -> None:
        if value:
            if isinstance(value, ModelABC):
                self._model = value.__class__
            elif issubclass(value, ModelABC):
                self._model = value
            else:
                raise TypeError()

    @property
    def open_directory(self) -> Any:
        """A :class:`OpenDirectoryABC` subclass used for the connection for the
        query.

        """
        return getattr(self, '_open_directory', None)

    @open_directory.setter
    def open_directory(self, value) -> None:
        if value is not None:
            if isinstance(value, OpenDirectoryABC):
                self._open_directory = value
            else:
                raise TypeError(value)

    @property
    def search_base(self) -> Union[str, None]:
        """A string representing where to search.

        This property will try to derive this value from several places.  If
        it set explicitly, then that will be the preferred return value.

        If it is not set explicitly, then we will check if there is an
        :class:`OpenDirectory` set for the instance. If so we will use the
        ``base_dn`` property from the ``open_directory``.  We will further
        check if a ``model`` has been set for the instance and we will add it's
        ``query_cn``.


        """
        search_base = getattr(self, '_search_base', None)
        if search_base is None:
            od_base = None
            try:
                od_base = self.open_directory.base_dn
            except AttributeError:
                pass

            model_cn = None
            try:
                model_cn = self.model.query_cn()
            except AttributeError:
                pass

            if model_cn is not None and od_base is not None:
                if "cn=" not in model_cn:
                    search_base = 'cn={},{}'.format(model_cn, od_base)
                else:
                    search_base = model_cn + ',{}'.format(od_base)
            elif od_base is not None:
                search_base = od_base

        return search_base

    @search_base.setter
    def search_base(self, value) -> None:
        if value is not None:
            self._search_base = str(value)

    @property
    def search_filter(self) -> str:
        """The ldap filter string for the query.  If not set then we will
        return the class's ``_default_search_filter`` which is '(objectClass=*)'

        """
        search_filter = getattr(self, '_search_filter', None)
        if search_filter is not None:
            return str(search_filter)
        return self._default_search_filter

    @search_filter.setter
    def search_filter(self, value) -> None:
        if value is not None:
            self._search_filter = str(value)

    @property
    def ldap_attributes(self) -> Union[None, Iterable[str]]:
        """The ldap attributes to return with the query.  These should be a
        list/tuple of strings that are attributes in the ldap database.

        If none have been set explicitly on an instance, then we will check if
        there is a ``model``, and use it's ``ldap_keys`` for this value.

        """
        attrs = getattr(self, '_ldap_attributes', None)
        if attrs is None:
            try:
                attrs = self.model.ldap_keys()
            except AttributeError:
                pass
        if attrs is not None:
            return tuple(attrs)

    @ldap_attributes.setter
    def ldap_attributes(self, value) -> None:
        if value is not None:
            if not isinstance(value, str):
                self._ldap_attributes = [s for s in iter(value)
                                         if isinstance(s, str)]
            else:
                self._ldap_attributes = [value]

    @property
    def connection(self) -> ConnectionCtx:
        """An :class:`ldap3.Connection` for the query.  If this is not set
        explicitly, then we will see if an ``open_directory`` is set on the
        instance and return it's ``connection``, which could still be ``None``,
        if there is no flask application running.

        If you don't know wheter you are working inside of the application
        context or not, then it is safer to use the
        :meth:`BaseQuery.connection_ctx` method.

        :raises TypeError:  If explicitly setting this to something other than
                            an :class:`ldap3.Connection`.

        """
        connection = getattr(self, '_connection', None)
        if connection is None:
            try:
                connection = self.open_directory.connection
            except AttributeError:
                pass
        return connection

    @connection.setter
    def connection(self, value):
        if value:
            if isinstance(value, ldap3.Connection):
                self._connection = value
            else:
                raise TypeError()

    @contextmanager
    def connection_ctx(self) -> Union[ldap3.Connection, None]:
        """A context manager that tries to find a connection to use.  If a
        connection is found on the instance or the ``open_directory`` of an
        instance, then that will be used.  If not it will try to create one
        using an instances ``open_directory``.

        If a connection is not able to be found this will yield ``None``, so
        you should check before using the connection.

        Example::

            >>> with query.connection_ctx() as conn:
            ...     model = query.first(conn)

        """
        if self.connection is not None:
            yield self.connection
        elif self.open_directory is not None:
            with self.open_directory.connection_ctx() as connection:
                yield connection
        else:
            yield

    def _query(self, connection) -> Iterable[ldap3.Entry]:
        """Helper that performs the query and yields :class:`ldap3.Entry`'s

        """
        if connection is not None:
            self.connection = connection

        with self.connection_ctx() as conn:
            if conn is not None:
                conn.search(
                    self.search_base,
                    self.search_filter,
                    attributes=self.ldap_attributes
                )
                for entry in conn.entries:
                    # check the entries have values. All attributes get returned
                    # as a list, so we check that the list has a length greater
                    # than 0.  This is useful, because when using the ``all``
                    # method, without any filter criteria, the first record is
                    # always empty lists.
                    if any(map(lambda x: len(x) > 0,
                               entry.entry_attributes_as_dict.values())):
                        yield entry
            # We should probably raise a connection error of some
            # sort here.

    def first(self, connection: ldap3.Connection=None, convert=True) -> Any:
        """Query the connection and return the first item found for the current
        state of the query.  This will return ``None`` if a connection was not
        established or there was no entry to match the filter criteria.

        :param connection:  An optional :class:`ldap3.Connection` to use for the
                            search.
        :param convert:  Whether to convert the :class:`ldap3.Entry` to the
                         ``model`` set on a class.  Default is ``True``

        """
        entry = next(self._query(connection), None)
        if convert is True and self.model is not None:
            return self.model.from_entry(entry)
        return entry

    def all(self, connection: ldap3.Connection=None, convert=True
            ) -> Tuple[Any]:
        """Query the connection and return a tuple of all items found for the
        current state of the query.  This will return an empty tuple if a
        connection was not established or there was no entries to match the
        filter criteria.

        :param connection:  An optional :class:`ldap3.Connection` to use for the
                            search.
        :param convert:  Whether to convert the :class:`ldap3.Entry`'s to the
                         ``model`` set on a class.  Default is ``True``

        """
        entries = tuple(self._query(connection))
        if len(entries) > 0:
            if convert is True and self.model is not None:
                return tuple(map(self.model.from_entry, entries))
        return entries

    def __repr__(self) -> str:
        rv = '{}('.format(self.__class__.__name__)
        attrs = map(
            lambda k: "{}={}".format(k, _quote_if_str(getattr(self, k, None))),
            ('search_base', 'search_filter', 'ldap_attributes', 'connection',
             'open_directory', 'model')
        )
        return rv + ', '.join(attrs) + ')'
