# -*- coding: utf-8 -*-

from typing import Dict, Union, Iterable
from .model_abc import ModelABC


def _quote_if_str(val):
    """Helper used in __repr__ statements

    """
    if isinstance(val, str):
        return "'{}'".format(val)
    return val


class Attribute(object):
    """Represents an LDAP entry attribute.  It maps the ldap entry key to an
    attribute on a Model.

    :param ldap_key:  The ldap entry key for the attribute.
    :param allow_multiple:  If ``False`` (default) then any lists only return
                            the first item.  If ``True`` return the whole list
                            of values.

    """
    def __init__(self, ldap_key, allow_multiple=False):
        self.ldap_key = ldap_key
        self.allow_multiple = allow_multiple

    def __str__(self):
        return str(self.ldap_key)

    def __repr__(self):
        return "{}('{}', allow_multiple={})".format(
            self.__class__.__name__,
            self.ldap_key,
            self.allow_multiple
        )


class BaseModel(ModelABC):
    """Implementation of :class:`ModelABC`.  Used to map ldap entry keys to
    python attributes.

    :param kwargs:  Values to set for the attributes of an instance.  These
                    can be passed in with the python attribute name as the key
                    or the ldap entry name as the key and the values will be
                    stored and accessible appropriately.


    :Example:

        >>> class User(BaseModel):
        ...     id = Attribute('apple-generateduid')
        >>> user = User(id='123')
        >>> user.id == '123'
        True
        >>> user2 = User(**{'apple-generateduid': '456'})
        >>> user2.id == '456'
        True


    """
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def _attributes(cls):
        """Returns the :class:`Attribute` instances on a class

        """
        return (v for v in vars(cls).values() if isinstance(v, Attribute))

    @classmethod
    def attribute_for_key(cls, key: str) -> Union[Attribute, None]:
        """Return :class:`Attribute` for the given key, which can be the python
        attribute or the ldap entry key.

        Returns ``None`` if not found

        """
        if key in cls.ldap_attribute_map().values():
            key = cls.attribute_name_for(key)
        return next((v for (k, v) in vars(cls).items() if k == key), None)

    @classmethod
    def ldap_attribute_map(cls) -> Dict[str, str]:
        """Returns the mapping between python attributes and ldap entry keys.

        The python attribute name is the key and ldap entry key is the value
        in the mapping.

        """
        return {k: v.ldap_key for (k, v) in vars(cls).items()
                if isinstance(v, Attribute)}

    @property
    def ldap_values(self) -> Dict[str, Union[str, Iterable[str]]]:
        """Stores the actual values for the :class:`Attribute`.  These are
        the values returned when accessing an :class:`Attribute` instance set
        on a Model.

        """
        if not getattr(self, '_ldap_values', None):
            self._ldap_values = {}
        return self._ldap_values

    def _get_ldap_value(self, key) -> Union[Iterable[str], str, None]:
        """Helper to get the internal value (if available) from the internal
        storage.

        """
        value = self.ldap_values.get(key)
        if value and object.__getattribute__(self, key).allow_multiple is False:
            if isinstance(value, list) and len(value) > 0:
                return value[0]
        return value

    def __setattr__(self, key, value) -> None:
        """Properly set the :class:`Attribute` values in the internal storage,
        or fallback to the default implementation.

        """
        if key in self.ldap_attribute_map().keys():
            self.ldap_values[key] = value
        elif key in self.ldap_attribute_map().values():
            self.ldap_values[self.attribute_name_for(key)] = value
        else:
            super().__setattr__(key, value)

    def __getattribute__(self, key):
        """Retrieve the appropriate values for an attribute, possibly from
        the internal storage, if the attribute being accessed is a
        :class:`Attribute`.

        """
        ldap_key = None
        attr_map = object.__getattribute__(self, 'ldap_attribute_map')()
        if key in attr_map.keys():
            ldap_key = key
        elif key in attr_map.values():
            ldap_key = object.__getattribute__(self, 'attribute_name_for')(key)
        if ldap_key is not None:
            # return the ldap value or ``None`` if it's not set yet.
            return object.__getattribute__(self, '_get_ldap_value')(ldap_key)
        # fallback to default
        return object.__getattribute__(self, key)

    def __repr__(self) -> str:
        rv = '{}('.format(self.__class__.__name__)
        attr_strs = map(
            lambda key: "{}={}".format(
                key,
                _quote_if_str(self._get_ldap_value(key))
            ),
            self.ldap_attribute_map().keys()
        )
        rv += ', '.join(attr_strs) + ')'
        return rv
