import flask
from flask import g

from notato.auth import requires_auth
from notato.models import Note
from notato import app

@app.route('/', endpoint='index')
@app.route('/notes/', endpoint='notes')
@app.route('/notes/create/', methods=['GET', 'POST'])
@requires_auth
def create_note():
    if flask.request.method == 'POST':
        form = flask.request.form
        note = Note()
        note.title = form.get('note_title', '').strip()
        note.text = form.get('note_text', '')
        note.markdown = True if form.get('markdown') else False
        note.public =  True if form.get('public') else False
        g.repo.save(note)
        flask.flash('Created new note.', 'success')
        
        target = form.get('target_state','edit')
        if target == 'read':
            return flask.redirect(flask.url_for('read_note', note_id=note.id))
        return flask.render_template('edit_note.html', note=note)

    return flask.render_template('create_note.html')

@app.route('/notes/read/<int:note_id>')
@requires_auth
def read_note(note_id):
    note = g.repo.get(note_id)
    if not note:
        flask.abort(404)
    return flask.render_template('read_note.html', note=note)

@app.route('/notes/read/<int:note_id>.raw')
@requires_auth
def read_note_raw(note_id):
    note = g.repo.get(note_id)
    if not note: 
        flask.abort(404)
    content = "# " + note.title_or_placeholder + "\n\n" + note.text
    return flask.Response(content, 200, {'content-type': 'text/plain'})

@app.route('/notes/edit/<int:note_id>', methods=['GET', 'POST'])
@requires_auth
def edit_note(note_id):
    note = g.repo.get(note_id)
    if not note:
        flask.abort(404)
    
    if flask.request.method == 'POST':
        form = flask.request.form
        note = Note(note_id)
        note.title = form.get('note_title', '').strip()
        note.text = form.get('note_text', '')
        note.markdown = True if form.get('markdown') else False
        note.public =  True if form.get('public') else False
        g.repo.save(note)
        flask.flash('Note was saved.', 'success')
        
        target = form.get('target_state','edit')
        if target == 'read':
            return flask.redirect(flask.url_for('read_note', note_id=note.id))

    return flask.render_template('edit_note.html', note=note)

@app.route('/notes/delete/<int:note_id>')
@requires_auth
def delete_note(note_id):
    g.repo.delete(note_id)
    flask.flash('Note was deleted.', 'success')
    return flask.redirect(flask.url_for('index'))

@app.route('/notes/public/')
def public_notes_list():
    note_ids = g.repo.get_public_ids()
    return flask.render_template('public_notes_list.html', note_ids=note_ids)

@app.route('/notes/public/<int:note_id>')
def public_note(note_id):
    note = g.repo.get(note_id)
    if not note.public:
        flask.abort(404)
    return flask.render_template('public_note.html', note=note)
