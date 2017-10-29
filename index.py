from flask import Flask, g, session, request
from flask_cors import CORS 
import json

import store
import authenticate as auth


app = Flask(__name__)
CORS(app)

# @app.before_request
# def lookup_current_user():
    # g.user = None
    # auth_token = request.headers['authorization']

    # console.log(auth_token)

    # if auth_token:
    #     # Check for authenticate token.
    #     # If token exists return user's information
    #     data = json.load(auth_token)
    #     g.user = auth.get_user(data.user_id)

    # # Default user, unauthenticated user, is None.
    # return

@app.route('/login', methods=['GET', 'POST'])
def login():
    # User already logged in.
    if g.user is not None:
        return redirect('http://localhost:4200')

    user_id = auth.check_auth(username, password)

    if user_id >= 0:
        # Response authenticate token.
        response = {}
        response['user_id'] = user_id
        response.headers['']
        return json.dumps(response)

    # Else, return unauthenticated message.
    return auth.auth_failed()


@app.route('/signup', methods=['POST'])
def signup():
    # User already logged in cannot create a new profile.
    if request.method == 'POST':
        print(request.get_json())
        data = request.get_json()

        # Store user information
        # TODO: Remove separators from username and password.
        username = data['username']
        password = data['password']
        age = data['age']
        gender = data['gender']

        print(username)

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
