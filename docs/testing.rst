Running Tests
=============


The tests for this package, currently, must be ran on your local machine.
There should be a working ``OpenDirectory`` environment with proper DNS set-up, 
and this package needs a few environment variables set in order to run the tests 
properly.


The Following Environment Variables are Needed for Testing::

    ##########################
    # CONFIGURATION VARIABLES
    ##########################

    OPEN_DIRECTORY_SERVER  # defaults to local host 

    # optional see also configuration
    OPEN_DIRECTORY_BASE_DN

    ############################
    # TESTING SPECIFIC VARIABLES
    ############################

    # a username used in a lot of the tests that require a user.
    # this user should also be a part of the ``OPEN_DIRECTORY_TEST_GROUP``
    OPEN_DIRECTORY_TEST_USERNAME  # defaults to 'testuser'

    # the ``OPEN_DIRECTORY_TEST_USERNAME``'s full name
    OPEN_DIRECTORY_TEST_USER_FULL_NAME  # defaults to 'Test User'

    # the ``OPEN_DIRECTORY_TEST_USERNAME``'s email address
    OPEN_DIRECTORY_TEST_USER_EMAIL  # defaults to 'test_user@example.com'

    # a group that the ``OPEN_DIRECTORY_TEST_USERNAME`` is a member of
    OPEN_DIRECTORY_TEST_GROUP  # defaults to 'testgroup'

    # a username that is part of macOS server's ``workgroup``, but not a member
    # of the ``OPEN_DIRECTORY_TEST_GROUP``
    OPEN_DIRECTORY_TEST_WORKGROUP_USERNAME  # defaults to testuser2

