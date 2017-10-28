from functools import wraps
from flask import request, Response
import storefrom flask import Flask, g, session
from flask.ext.openid import OpenID
from flask.ext.openid import OpenID


def check_auth(username, password):
    auths = store.get_users()
    return auths.loc[df['username'] == username and df['password'] == password]

def auth_failed():
    """Sends a 401 response that enables basic auth"""

    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password)
            return auth_failed()
        return f(*arg, **kwargs)
    return decorated



def sign_up(username, password):
    # Try to find username in store.
    if username not found:
        store.add_user(username, password)

    # If username has already exist return failed.
    if store.exists_user:
        return false

    # Else save username and password into the store.
