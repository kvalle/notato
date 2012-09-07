from flask import g
import flask
import markdown

import auth
import repo

from notato.models import Note
from notato import app

@app.route('/', endpoint='index')
@app.route('/notes/', endpoint='notes')
@app.route('/notes/create/')
@auth.requires_auth
def create_note():
    note = Note(note_id=repo.next_id())
    return flask.render_template('edit_note.html', page_title='Create note', note=note)

@app.route('/notes/read/<int:note_id>')
@auth.requires_auth
def read_note(note_id):
    note = g.repo.get(note_id)
    if not note:
        flask.abort(404)
    return flask.render_template('read_note.html', note=note)

@app.route('/notes/read/<int:note_id>.raw')
@auth.requires_auth
def read_note_raw(note_id):
    note = g.repo.get(note_id)
    if not note: 
        flask.abort(404)
    content = "# " + note.title + "\n\n" + note.text
    return flask.Response(content, 200, {'content-type': 'text/plain'})

@app.route('/notes/edit/<int:note_id>', methods=['GET', 'POST'])
@auth.requires_auth
def edit_note(note_id):
    target = 'edit'
    if flask.request.method == 'POST':
        title = flask.request.form.get('note_title', '').strip()
        text = flask.request.form.get('note_text', '')
        markdown = True if flask.request.form.get('markdown') else False
        target = flask.request.form.get('target_state','edit')
        note = Note(note_id, title, text, markdown=markdown)
        g.repo.save(note)
        flask.flash('Note was saved.', 'success')
    else:
        note = g.repo.get(note_id)
        if not note: 
            flask.abort(404)
    if target == 'read':
        return flask.redirect(flask.url_for('read_note', note_id=note.id))
    else:
        return flask.render_template('edit_note.html', page_title='Edit note', note=note)

@app.route('/notes/delete/<int:note_id>')
@auth.requires_auth
def delete_note(note_id):
    g.repo.delete(note_id)
    flask.flash('Note was deleted.', 'success')
    return flask.redirect(flask.url_for('index'))

@app.route('/about/')
@auth.requires_auth
def about():
    return flask.render_template('about.html')

@app.errorhandler(404)
def page_not_found(e):
    return flask.render_template('404.html'), 404
    
@app.route('/log-in', methods=['GET', 'POST'])
def login():
    username = ""
    if flask.request.method == 'POST':
        username = flask.request.form['username']
        password = flask.request.form['password']
        if auth.login(username, password):
            flask.flash('You were logged in.', 'success')
            next_page = flask.session.pop('next_page', flask.url_for('index'))
            return flask.redirect(next_page)
        else:
            flask.flash('Invalid username or password.', 'error')
    return flask.render_template('login.html', username=username)

@app.route('/log-out')
def logout():
    auth.logout()
    flask.flash('You were logged out.', 'success')
    return flask.redirect(flask.url_for('login'))

