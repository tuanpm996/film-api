from flask import Flask, g, session, request
from flask.ext.openid import OpenID

import store
from store import oid
import authenticate as auth

app = Flask(__name__)

@app.before_request
def lookup_current_user():
    g.user = None
    if 'openid' in session:
        openid = request.get_json()['openid']
        g.user = store.get_user(openid)

@app.route('/login')
@oid.loginhandler
def login():
    if g.user is not None:
        return redirect('http://localhost:4200')

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if openid:
            return oid.try_login(openid, ask_for=['username', 'password'],
                                         ask_for_optional=['fullname'])
    return render_template('login.html', next=oid.get_next_url(),
                           error=oid.fetch_error())

@app.route('/signup')
def signup():
    if g.user is not None:
        return redirect('http://localhost:4200')

    if request.method == 'POST'
        username = request.form.get('username')
        password = request.form.get('password')

        if auth.signup(username, password):
            # TODO: Add signup method.
    
    return redirect('http://localhost:4200/login')

@app.route('/logout')
def logout():
    session.pop('openid', true)
    return redirect('http://localhost:4200')

@app.route('/films')
def get_films():
    return store.get_films()