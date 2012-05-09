from functools import wraps
from flask import Flask, request, Response, render_template, abort, redirect, url_for
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

def note_ids():
    return sorted(map(int, os.listdir('storage')))

@app.route('/', methods=['GET', 'POST'])
@requires_auth
def index():
    return render_template('index.html',note_ids=note_ids())

def note_file_name(note_id):
    return os.path.join('storage',str(note_id))

def is_note(note_id):
    return os.path.isfile(note_file_name(note_id))

def write_note(note_id, text):
    with open(note_file_name(note_id), 'w') as note:
        note.write(text)

def read_note(note_id):
    if not is_note(note_id):
        return ""
    with open(note_file_name(note_id), 'r') as note:
        return note.read()

@app.route('/note/<int:note_id>', methods=['GET', 'POST'])
@requires_auth
def edit_note(note_id):
    if request.method == 'POST':
        text = request.form['note']
        write_note(note_id, text)
    else:
        text = read_note(note_id)
    return render_template('note.html', text=text, note_id=note_id)

@app.route('/note/new')
@requires_auth
def new_note():
    existing = note_ids()
    next = 1
    while next in existing:
        next += 1
    note_url = url_for('edit_note', note_id=next)
    return redirect(note_url)

@app.route('/note/delete/<int:note_id>')
@requires_auth
def delete_note(note_id):
    os.remove(note_file_name(note_id))
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)

