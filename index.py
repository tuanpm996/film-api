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
                'user_id': -1
            }
            try:
                data['user_id'] = int(decoded_token)
            except json.JSONDecodeError as e:
                print(e)

            g.user = store.get_user(data['user_id'])
            print(g.user)
    # Default user, unauthenticated user, is None.


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
    return store.get_films()  \
        .loc[3:8]             \
        .to_json(orient='records')

@app.route('/film/<id>', methods=['GET', 'POST'])
def get_film(id):
    record = store.get_film_by_id(int(id))

    return json.dumps(record)

@app.route('/suggest', methods=['GET'])
def suggest_empty():
    films = store.get_films()

    return films.loc[3:8] \
        .to_json(orient='records')

@app.route('/suggest/<raw_string>', methods=['GET'])
def suggest(raw_string):
    decoded_string = base64.b64decode(raw_string).decode('UTF-8')

    films = store.get_films()

    return films.loc[films['name'].str          \
        .contains(decoded_string, na=False)]    \
        .to_json(orient='records')


@app.route('/search/<raw_string>', methods=['GET'])
def search(raw_string):
    decoded_string = base64.b64decode(raw_string).decode('UTF-8')

    films = store.get_films()

    return films.loc[
            films['name'].str
            .contains(decoded_string, na=False)
        ]           \
        .to_json(orient='records')
