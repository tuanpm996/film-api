from functools import wraps
from flask import request, Response, Flask, g, session, redirect
import json

import store
import response as res


def check_auth(username, password):
    users = store.get_users()
    df = users.loc[store.auth_cache['username'].isin([username])]

    print(df['password'].isin([password]).iloc[0])

    if df['password'].isin([password]).iloc[0]:
        return df.index[0]
    else:
        return -1
    
def auth_failed():
    """Sends a 401 response that enables basic auth"""

    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

def sign_up(username, password, user_info):
    # Try to find username in store.
    if store.exists_user(username):
        
        # If username has already exist return failed.
        return auth_failed()

    # Else save username and password into the store.
    store.add_user(username, password, user_info)

    return res.status_ok()
