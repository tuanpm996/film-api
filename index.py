from flask import Flask, g, session, request
import json

import store
import authenticate as auth

app = Flask(__name__)

@app.before_request
def lookup_current_user():
    g.user = None
    data = request.to_json()
    
    if data is not None and data.user_id is not None:
        # Check for authenticate token.
        # If token exists return user's information
        g.user = auth.get_user(data.user_id)

    # Default user, unauthenticated user, is None.


@app.post('/login')
def login():
    # User already logged in.
    if g.user is not None:
        return redirect('http://localhost:4200')

    username = request.form.get('username')
    password = request.form.get('password')

    user_id = auth.check_auth(username, password)
    if user_id:
        # Response authenticate token.
        response = {}
        response['user_id'] = user_id
        return response

    # Else, return unauthenticated message.
    return auth.auth_failed()


@app.post('/signup')
def signup():
    # User already logged in cannot create a new profile.
    if g.user is not None:
        return redirect('http://localhost:4200')

    # TODO: Store user information
    username = request.form.get('username')
    password = request.form.get('password')

    store.add_user(username, password)

    return redirect('http://localhost:4200/login')


@app.get('/films')
def get_films():
    return store.get_films()

@app.get('/film/:id')
def get_film():
    id = request.args.get('id', type=int, default=None)
    return store.get_film(id)