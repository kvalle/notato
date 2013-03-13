import os, os.path
import mimetypes

import flask
from flask import g
import werkzeug

from notato.auth import requires_auth
from notato.models import Note
from notato import app

ignorefiles = ['.gitignore']

@app.route('/files/', methods=['GET'])
@requires_auth
def files():
    files = os.listdir(app.config['FILES_DIR'])
    files = filter(lambda f: f not in ignorefiles, files)
    return flask.render_template('files.html', files=files)

@app.route('/files/upload/', methods=['GET', 'POST'])
@requires_auth
def upload_file():
    if flask.request.method == 'POST':
        f = flask.request.files['new_file']
        if not f:
            flask.flash('No file specified', 'warning')
        else:
            filename = werkzeug.secure_filename(f.filename)
            path = app.config['FILES_DIR'] + filename
            f.save(path)
            flask.flash('Successfully uploaded "%s"' % filename, 'success')
    return flask.redirect(flask.url_for('files'))

@app.route('/files/raw/<string:filename>')
@requires_auth
def raw_file(filename):
    path = app.config['FILES_DIR'] + filename
    if not os.path.exists(path):
        flask.abort(404)
    with open(path, 'r') as f:
        content = f.read()
    mimetype, _ = mimetypes.guess_type(filename)
    return flask.Response(content, 200, {'content-type': mimetype or 'text/plain'})

@app.route('/files/delete/<string:filename>')
@requires_auth
def delete_file(filename):
    path = app.config['FILES_DIR'] + filename
    if not os.path.exists(path):
        flask.abort(404)
    os.remove(path)
    flask.flash('Successfully deleted "%s"' % filename, 'success')
    return flask.redirect(flask.url_for('files'))
