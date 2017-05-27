#!/usr/bin/env python
"""

A custom model example for an ``OpenDirectory`` computer group.

"""
from flask_open_directory import BaseModel, Attribute


class ComputerGroup(BaseModel):
    """Represents an ``OpenDirectory`` computer group

    """
    id = Attribute('apple-generateduid')
    """The id for a computer group."""

    computer_names = Attribute('memberUid', allow_multiple=True)
    """A list of the computer name(s) that are members of the group."""

    computer_ids = Attribute('apple-group-memberguid', allow_multiple=True)
    """A list of the computer id(s) that are members of the group."""

    def has_computer(self, computer: str) -> bool:
        """Check if the computer is a member of the group.

        :param computer:  A computer name or computer id to check membership.

        """
        if self.computer_names and computer in self.computer_names:
            return True
        if self.computer_ids and computer in self.computer_ids:
            return True
        return False

    @classmethod
    def query_cn(cls) -> str:
        """Return the query cn used for searches.

        """
        return 'cn=computer_groups'


if __name__ == '__main__':

    from flask_open_directory import OpenDirectory

    open_directory = OpenDirectory()

    computers = open_directory.query(ComputerGroup).all()
    print('computers', computers)

    if len(computers) > 0:
        for c in computers:
            assert isinstance(c, ComputerGroup)
            assert isinstance(c.id, str)
            assert isinstance(c.computer_ids, list)
            assert isinstance(c.computer_names, list)
