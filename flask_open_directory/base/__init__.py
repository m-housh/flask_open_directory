# -*- coding: utf-8 -*-
from typing import Union, ContextManager
from flask import _app_ctx_stack
from contextlib import contextmanager
import ldap3

from .open_directory_abc import OpenDirectoryABC
from .. import utils


__all__ = ('OpenDirectoryABC', 'BaseOpenDirectory')


class BaseOpenDirectory(OpenDirectoryABC):
    """Implements the :class:`OpenDirectoryABC`.

    This stores all kwargs into a ``config`` attribute, which is used to
    get the server url and an optional base dn.

    """
    _default_server = 'localhost'
    _default_base_dn = ''

    def __init__(self, **config):
        self.config = config

    @property
    def server_url(self) -> str:
        """Return the server url for an instance.  This looks in the ``config``
        dict for key 'OPEN_DIRECTORY_SERVER' and if noting is found it
        returns ``_default_server`` set on the class (default 'localhost').

        """
        return self.config.get('OPEN_DIRECTORY_SERVER', self._default_server)

    @property
    def base_dn(self) -> str:
        """Return the base dn for the open directory server.  This looks in the
        ``config`` dict for key 'OPEN_DIRECTORY_BASE_DN' and if nothing is found
        it will create one from the ``server_url``.

        .. note::
            If your server url is an ip address, then you need to set this in
            the config.

        """
        rv = self.config.get('OPEN_DIRECTORY_BASE_DN', None)
        if rv is None:
            rv = utils.base_dn_from_url(self.server_url)
        return rv or self._default_base_dn

    def create_server(self) -> ldap3.Server:
        """Create's a :class:`ldap3.Server` with this instances ``server_url``.
        This method is typically only used internally.

        """
        return ldap3.Server(self.server_url, use_ssl=True)

    def connect(self) -> ldap3.Connection:
        """Create's an :class:`ldap3.Connection`, that will need to be managed
        by the caller (closed, cleanup, etc).  This is primarily used when there
        is a flask application running.  It is better to use the
        ``connection_ctx`` context manager.

        """
        return ldap3.Connection(
            self.create_server(),
            auto_bind=True
        )

    @property
    def connection(self) -> Union[None, ldap3.Connection]:
        """Return's a shared connection when a flask application is running.
        If there is not flask application running, then this property will
        return ``None``.

        If you need a connection outside of a flask application context, then
        you can create one with the ``connect`` method or use the
        ``connection_ctx`` method, which works the same with or without an
        application context.

        """
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'open_directory_connection'):
                ctx.open_directory_connection = self.connect()
            return ctx.open_directory_connection

    @contextmanager
    def connection_ctx(self) -> ContextManager[ldap3.Connection]:
        """A context manager that will use the shared connection if a flask
        application context is available if not it will create a connection
        for running one-off commands.

        """
        if self.connection is not None:
            yield self.connection
        else:
            with ldap3.Connection(self.create_server()) as connection:
                yield connection
