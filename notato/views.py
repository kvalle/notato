from flask import g
import flask
import markdown

import config
import auth
import repo

from notato import app

@app.route('/')
@auth.requires_auth
def index():
    return flask.redirect(flask.url_for('notes'))

@app.route('/note/')
@auth.requires_auth
def notes():
    if g.note_ids:
        first_id = g.note_ids[0]
        return flask.redirect(flask.url_for('read_note', note_id=first_id))
    return flask.redirect(flask.url_for('create_note'))

@app.route('/note/create/')
@auth.requires_auth
def create_note():
    n = repo.Note(nid=repo.next_id())
    return flask.render_template('edit_note.html', page_title='Create note', note=n)

@app.route('/note/read/<int:note_id>')
@auth.requires_auth
def read_note(note_id):
    if not repo.is_note(note_id):
        flask.abort(404)
    n = repo.read(note_id)
    if not n.title:
        n.title = 'untitled note'
    n.html = markdown.markdown(n.text)
    return flask.render_template('read_note.html', note=n)

@app.route('/note/read/<int:note_id>.raw')
@auth.requires_auth
def read_note_raw(note_id):
    if not repo.is_note(note_id):
        flask.abort(404)
    n = repo.read(note_id)
    return flask.Response(n.text, 200, {'content-type': 'text/plain'})

@app.route('/note/edit/<int:note_id>', methods=['GET', 'POST'])
@auth.requires_auth
def edit_note(note_id):
    target = 'edit'
    if flask.request.method == 'POST':
        note_title = flask.request.form.get('note_title', '').strip()
        note_text = flask.request.form.get('note_text', '')
        target = flask.request.form.get('target_state','edit')
        n = repo.Note(note_id, note_title, note_text)
        repo.write(n)
        flask.flash('Note %d was successfully saved.' % note_id)
    else:
        if not repo.is_note(note_id):
            flask.abort(404)
        n = repo.read(note_id)
    if target == 'read':
        return flask.redirect(flask.url_for('read_note', note_id=n.id))
    else:
        return flask.render_template('edit_note.html', page_title='Edit note', note=n)

@app.route('/note/delete/<int:note_id>')
@auth.requires_auth
def delete_note(note_id):
    if not repo.is_note(note_id):
        flask.abort(404)
    repo.delete(note_id)
    flask.flash('Note %d was successfully deleted.' % note_id)
    return flask.redirect(flask.url_for('index'))

@app.route('/about/')
@auth.requires_auth
def about():
    return flask.render_template('about.html')

