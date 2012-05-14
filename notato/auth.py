import hashlib
from functools import wraps
from flask import Response, request
import flask
import config
from notato import app
from flask import g

def login(username, password):
    if not _check(username, password): 
        return False
    flask.session['logged_in'] = True
    return True

def logout():
    flask.session.pop('logged_in', None)

def _check(username, password):
    if not username == config.USERNAME:
        return False
    return config.PASSWORD == hashlib.sha1(password).hexdigest()

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not flask.session.get('logged_in', False):
            flask.flash("You must log in to view this page.")
            return flask.redirect(flask.url_for('login'))
        return f(*args, **kwargs)
    return decorated
