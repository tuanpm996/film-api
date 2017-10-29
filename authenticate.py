from functools import wraps
from flask import request, Response, Flask, g, session

import store


def check_auth(username, password):
    users = store.get_users()
    df = users.loc[df['username'].isin([username])]
    
    if (df.loc['password'] == password)[0]:
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

    return redirect('http://localhost:4200/login')
