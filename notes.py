from functools import wraps
from flask import Flask, request, Response, render_template, abort
import os.path

app = Flask(__name__)

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'password'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/', methods=['GET', 'POST'])
@requires_auth
def index():
    return render_template('index.html')

def note_file_name(num):
    return 'storage/note-'+str(num)

def is_note(num):
    return os.path.isfile(note_file_name(num))

def write_note(num, text):
    with open(note_file_name(num), 'w') as note:
        note.write(text)

def read_note(num):
    with open(note_file_name(num), 'r') as note:
        return note.read()

@app.route('/note/<int:note_id>', methods=['GET', 'POST'])
@requires_auth
def note(note_id):
    if not is_note(note_id):
        abort(404)
    if request.method == 'POST':
        text = request.form['note']
        write_note(note_id, text)
    else:
        text = read_note(note_id)
    return render_template('note.html', text=text)

if __name__ == "__main__":
    app.run(debug=True)
