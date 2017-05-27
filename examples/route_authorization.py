#!/usr/bin/env python
"""

route_authorization.py
----------------------

Example application using the authorization decorators.  This example would
require an ``OpenDirectory`` environment with an ``office`` and an
``adminstrators`` group.



"""
from flask import Flask
from flask_open_directory import OpenDirectory, requires_group, \
    requires_any_group, requires_all_groups, utils


app = Flask(__name__)

open_directory = OpenDirectory(app)


@app.route('/')
def index():
    return "Hello, you don't have to be authorized to access this page."


@app.route('/admins')
@requires_group('administrators')
def admins():
    return "Hello '{}', you must be an administrator.".format(
        utils.username_from_request()
    )


@app.route('/office-or-admins')
@requires_any_group('office', 'administrators')
def office_admins():
    return "Hello '{}', you must be an office or adminstrator member".format(
        utils.username_from_request()
    )


@app.route('/only-office-admins')
@requires_all_groups('office', 'administrators')
def only_office_admins():
    return "Hello '{}', you must be an office adminstrator.".format(
        utils.username_from_request()
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
