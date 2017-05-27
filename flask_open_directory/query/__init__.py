# -*- coding: utf-8 -*-
from typing import Union
from functools import wraps
import collections

from .query_abc import QueryABC
from .base_query import BaseQuery

__all__ = ('QueryABC', 'Query', 'BaseQuery')


def chainable_method(fn):
    """Marks a method to always return self/class regardless of wrapped
    method's output.

    """
    @wraps(fn)
    def decorator(self, *args, **kwargs):
        fn(self, *args, **kwargs)
        return self
    return decorator


class Query(BaseQuery):
    """Extends the :class:`BaseQuery` with some helper methods.  The helpers
    typically return the query when called for method chaining.

    This allows a query to be mostly setup by another object, and the caller
    provide the criteria for the search.

    Example::

        >>> query = Query(open_directory=OpenDirectory())
        >>> query(User).filter(username='testuser').first()
        User(...)
        >>> query.all()  # reuse the same criteria, only get all the users
        [User(...),
        ...]
        >>> q = query(Group)  # change the ``model`` on a query
        >>> q == query
        True
        >>> q.filter(group_name='testgroup').first()
        Group(...)

    """
    def _parse_filter_kwargs(self, kwargs):
        """Helper to yield '(key=value)' strings from kwargs.  This method also
        parses the key with the ``model`` attribute of an instance to get the
        correct key to use in the query.

        """
        if len(kwargs) > 0 and isinstance(kwargs, collections.Mapping):
            for key, value in kwargs.items():
                if self.model is not None:
                    mkey = self.model.attribute_for_key(key).ldap_key
                    if mkey is not None:
                        key = mkey
                yield '({}={})'.format(key, value)

    def _filter_string_from_kwargs(self, kwargs) -> Union[str, None]:
        """Helper to create the filter string from kwargs.

        """
        parsed = tuple(self._parse_filter_kwargs(kwargs))
        if len(parsed) > 1:
            return '(&' + ''.join(parsed) + ')'
        elif len(parsed) == 1:
            return parsed[0]

    @chainable_method
    def filter(self, *args, **kwargs) -> 'Query':
        """Set's the search filter for an instance, returning the query for
        method chaining.

        This method will accept a string or keyword arguments as parameters.

        If there is a string passed in it is set as the filter on the instance.
        There is no parsing or validation done on a string if it's passed in,
        which can cause errors when performing the query if it is an invalid
        filter string.

        If there is no string passed in then keyword arguments are parsed with
        the current ``model`` set on an instance.  This means that you can build
        a query using either the model's attribute name or the ldap entry key.

        :Example:

            >>> from open_directory_utils.model import User
            >>> from open_directory_utils.query import Query
            >>> q = Query(search_base='dc=example,dc=com', model=User)
            >>> q.filter(username='testuser')
            Query(...)
            >>> print(q.search_filter)
            '(uid=testuser)'
            >>> q.filter(uid='anotheruser')
            Query(...)
            >>> print(q.search_filter)
            '(uid=anotheruser)'
            >>> q.filter('(cn='Test User')')
            >>> print(q.search_filter)
            '(cn=Test User)'

        """
        string = next((s for s in iter(args) if isinstance(s, str)), None)
        if string is None and len(kwargs) > 0:
            string = self._filter_string_from_kwargs(kwargs)
        self.search_filter = string

    @chainable_method
    def __call__(self, model) -> 'Query':
        """Set/change the model for an instance.

        """
        self.model = model
