import flask

import config
import auth
import note

from notato import app

@app.route('/', methods=['GET', 'POST'])
@auth.requires_auth
def index():
    return flask.render_template('index.html', note_ids=note.list_ids())

@app.route('/note/create')
@auth.requires_auth
def create_note():
    existing = note.list_ids()
    next = 1
    while next in existing:
        next += 1
    note_url = flask.url_for('update_note', note_id=next)
    return flask.redirect(note_url)

@app.route('/note/<int:note_id>', methods=['GET', 'POST'])
@auth.requires_auth
def update_note(note_id):
    if flask.request.method == 'POST':
        text = flask.request.form['note']
        note.write(note_id, text)
        flask.flash('Note %d was successfully saved.' % note_id)
    else:
        text = note.read(note_id)
    return flask.render_template('note.html', text=text, note_id=note_id)

@app.route('/note/delete/<int:note_id>')
@auth.requires_auth
def delete_note(note_id):
    note.delete(note_id)
    flask.flash('Note %d was successfully deleted.' % note_id)
    return flask.redirect(flask.url_for('index'))

