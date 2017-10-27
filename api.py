from flask import Flask, session,render_template,redirect,url_for
from flask_restful import reqparse, abort, Api, Resource, request
import pdb;
import read;
import json;
app = Flask(__name__)
api = Api(app)
app.secret_key = 'super-secret-text'
# def abort_if_film_doesnt_exist(film_id):
#     if film_id not in FILMS:
#         abort(404, message="Film {} doesn't exist".format(todo_id))

# parser = reqparse.RequestParser()
# parser.add_argument('task')


# Todo
# shows a single todo item and lets you delete a todo item

@app.before_request
def do_something_whenever_a_request_comes_in():
    # pdb.set_trace();
    check_logged_in()

class Film(Resource):
    def get(self, film_id):
        # abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class FilmsList(Resource):
    def get(self):
        session['a'] = 'b'
        session.clear()
        pdb.set_trace();
        file = read.index().to_json(orient="records")
        file = json.loads(read.index().to_json(orient="records"))
        return file

    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201

##
## Actually setup the Api resource routing here
##
api.add_resource(FilmsList, '/films')
api.add_resource(Film, '/films/<film_id>/')
@app.route('/')
def home():
    return "fdfdfdf";

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if (request.form['username']=="1" and request.form['password']=="1"):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)

def log_the_user_in(username):
    session['username'] = username
    return redirect (url_for('filmslist'))

def check_logged_in():
    pdb.set_trace();
    if(session['username'] == None):
      return render_template('login.html', error="You must login")
if __name__ == '__main__':
    app.run(debug=False)
