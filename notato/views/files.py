import os

import flask
from flask import g
import werkzeug

from notato.auth import requires_auth
from notato.models import Note
from notato import app

@app.route('/files/', methods=['GET'])
@requires_auth
def files():
    files = os.listdir(app.config['FILES_DIR'])
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
