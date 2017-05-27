from .model_abc import ModelABC
from .model import BaseModel, Attribute


__all__ = ('ModelABC', 'BaseModel', 'Attribute', 'User', 'Group')


class User(BaseModel):
    """Represents a user in the open directory

    .. seealso:: :class:`BaseModel` for inherited methods.

    """
    id = Attribute('apple-generateduid')
    """The id (apple-generateduid) for a user."""

    username = Attribute('uid')
    """The username (uid/short-name) for a user"""

    email = Attribute('mail', allow_multiple=True)
    """The email address(s) (mail) for a user."""

    full_name = Attribute('cn')
    """The full name (cn) for the user"""


class Group(BaseModel):
    """Represents a group in the open directory

    .. seealso:: :class:`BaseModel` for inherited methods.

    """
    id = Attribute('apple-generateduid')
    """The id (apple-generateduid) for the group"""

    group_name = Attribute('cn')
    """The group name (cn) for the group"""

    full_name = Attribute('apple-group-realname')
    """The group full name (apple-group-realname) for the group"""

    users = Attribute('memberUid', allow_multiple=True)
    """The usernames (memberUid) that are members of the group"""

    member_ids = Attribute('apple-group-memberguid', allow_multiple=True)
    """The user(s) id's (apple-group-memberguid) of the group"""

    def has_user(self, user: str) -> bool:
        """Check if a user is part of the group.

        :param user:  Either the username (uid) or id (apple-generateduid) of
                      a user.

        """
        if self.users is not None:
            if user in self.users:
                return True
        if self.member_ids is not None:
            if user in self.member_ids:
                return True
        return False
