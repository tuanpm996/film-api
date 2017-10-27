from flask import Flask
import store

app = Flask(__name__)

@app.route("/films")
def get_films():
    return store.get_films()