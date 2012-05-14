from flask import g
import flask
import markdown

import config
import auth
import repo

from notato.models import Note
from notato import app

@app.route('/')
@auth.requires_auth
def index():
    return flask.redirect(flask.url_for('notes'))

@app.route('/log-in', methods=['GET', 'POST'])
def login():
    username = ""
    if flask.request.method == 'POST':
        username = flask.request.form['username']
        password = flask.request.form['password']
        if auth.login(username, password):
            flask.flash('You were successfully logged in.')
            return flask.redirect(flask.url_for('index'))
        else:
            flask.flash('Invalid username or password.')
    return flask.render_template('login.html', username=username)

@app.route('/log-out')
def logout():
    auth.logout()
    flask.flash('You were successfully logged out.')
    return flask.redirect(flask.url_for('login'))

@app.route('/note/')
@auth.requires_auth
def notes():
    if g.note_ids:
        return flask.redirect(flask.url_for('read_note', note_id=g.note_ids[0]))
    else:
        return flask.redirect(flask.url_for('create_note'))

@app.route('/note/create/')
@auth.requires_auth
def create_note():
    note = Note(note_id=repo.next_id())
    return flask.render_template('edit_note.html', page_title='Create note', note=note)

@app.route('/note/read/<int:note_id>')
@auth.requires_auth
def read_note(note_id):
    note = repo.get(note_id)
    if not note: 
        flask.abort(404)
    if not note.title:
        note.title = 'untitled note'
    note.html = markdown.markdown(note.text)
    return flask.render_template('read_note.html', note=note)

@app.route('/note/read/<int:note_id>.raw')
@auth.requires_auth
def read_note_raw(note_id):
    note = repo.get(note_id)
    if not note: 
        flask.abort(404)
    return flask.Response(note.text, 200, {'content-type': 'text/plain'})

@app.route('/note/edit/<int:note_id>', methods=['GET', 'POST'])
@auth.requires_auth
def edit_note(note_id):
    target = 'edit'
    if flask.request.method == 'POST':
        title = flask.request.form.get('note_title', '').strip()
        text = flask.request.form.get('note_text', '')
        target = flask.request.form.get('target_state','edit')
        note = Note(note_id, title, text)
        repo.save(note)
        flask.flash('Note was successfully saved.')
    else:
        note = repo.get(note_id)
        if not note: 
            flask.abort(404)
    if target == 'read':
        return flask.redirect(flask.url_for('read_note', note_id=note.id))
    else:
        return flask.render_template('edit_note.html', page_title='Edit note', note=note)

@app.route('/note/delete/<int:note_id>')
@auth.requires_auth
def delete_note(note_id):
    note = repo.get(note_id)
    if not note: 
        flask.abort(404)
    repo.delete(note.id)
    flask.flash('Note was successfully deleted.')
    return flask.redirect(flask.url_for('index'))

@app.route('/about/')
@auth.requires_auth
def about():
    return flask.render_template('about.html')

