#!/usr/bin/env python
"""
custom_decorator.py
-------------------

This example shows how to create a custom authorization decorator using the
``pass_context`` helper.

"""
from functools import wraps
from flask import abort, Flask
from flask_open_directory import pass_context, OpenDirectory


def only_username(username):
    """A silly example, that only allows the specified username to access
    the route.

    :param username:  The authorized username who can access the route.

    """
    def inner(fn):

        @wraps(fn)
        @pass_context
        def decorator(ctx, *args, **kwargs):
            request_username = ctx.username
            if request_username == username:
                return fn(*args, **kwargs)
            return abort(401)

        return decorator

    return inner


app = Flask(__name__)
open_directory = OpenDirectory(app)


@app.route('/george')
@only_username('george')
def george_only():

    return 'Hello, you must be George'


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, debug=True)
