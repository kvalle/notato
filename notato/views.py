import os.path
import flask

from notato import app
import config
import auth

def note_ids():
    return sorted(map(int, os.listdir(config.STORAGE)))

def note_file_name(note_id):
    return os.path.join(config.STORAGE, str(note_id))

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

@app.route('/', methods=['GET', 'POST'])
@auth.requires_auth
def index():
    return flask.render_template('index.html',note_ids=note_ids())

@app.route('/note/<int:note_id>', methods=['GET', 'POST'])
@auth.requires_auth
def edit_note(note_id):
    if flask.request.method == 'POST':
        text = flask.request.form['note']
        write_note(note_id, text)
        flask.flash('Note %d was saved.' % note_id)
    else:
        text = read_note(note_id)
    return flask.render_template('note.html', text=text, note_id=note_id)

@app.route('/note/new')
@auth.requires_auth
def new_note():
    existing = note_ids()
    next = 1
    while next in existing:
        next += 1
    note_url = flask.url_for('edit_note', note_id=next)
    return flask.redirect(note_url)

@app.route('/note/delete/<int:note_id>')
@auth.requires_auth
def delete_note(note_id):
    os.remove(note_file_name(note_id))
    flask.flash('Note %d deleted.' % note_id)
    return flask.redirect(flask.url_for('index'))

