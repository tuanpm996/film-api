from flask import Flask, g, session, request, redirect
from flask_cors import CORS 
import numpy as np
import json
import base64

import store
import authenticate as auth
import response as res


app = Flask(__name__)
CORS(app)

@app.before_request
def lookup_current_user():
    g.user = None

    if 'authorization' in request.headers:
        auth_token = request.headers['authorization']

        if auth_token is not None and auth_token != 'null':
            # Check for authenticate token.
            # If token exists return user's information
            decoded_token = base64.b64decode(auth_token).decode('UTF-8')
            print(decoded_token)
            data = {
                "user_id": -1
            }
            try:
                data = json.loads(decoded_token, encoding='UTF-8')
            except json.JSONDecodeError as e:
                print(e)
            g.user = store.get_user(data['user_id'])
            print(g.user)
    # Default user, unauthenticated user, is None.


@app.route('/login', methods=['GET', 'POST'])
def login():
    # User already logged in.
    if g.user is not None:
        return redirect('http://localhost:4200')

    data = request.get_json()

    username = data['username']
    password = data['password']

    user_id = auth.check_auth(username, password)

    if user_id >= 0:
        # Response authenticate token.
        return res.status_ok({
            'user_id': str(user_id),
            'username': username
        })

    # Else, return unauthenticated message.
    return auth.auth_failed()


@app.route('/signup', methods=['POST'])
def signup():
    print(request.get_json())
    data = request.get_json()

    # Store user information
    # TODO: Remove separators from username and password.
    username = data['username']
    password = data['password']
    age = data['age']
    gender = data['gender']

    print('{0} {1} {2} {3}'.format(username, password, age, gender))

    user_info = {}
    user_info['age'] = age
    user_info['gender'] = gender

    return auth.sign_up(username, password, user_info)


@app.route('/films', methods=['GET', 'POST'])
def get_films():
    print(g.user)
    return store.get_films()


@app.route('/film/:id', methods=['GET', 'POST'])
def get_film():
    print(g.user)
    id = request.args.get('id', type=int, default=None)
    return store.get_film(id)
