from functools import wraps
from flask import Response, request
import flask
import config
from notato import app
from flask import g

@app.before_request
def before_request():
    g.logged_in = flask.session.get('logged_in', False)

def login(username, password):
    if not _check(username, password): 
        return False
    flask.session['logged_in'] = True
    g.logged_in = True
    return True

def logout():
    flask.session.pop('logged_in', None)
    g.logged_in = False

def _check(username, password):
    return username == config.USERNAME and password == config.PASSWORD

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not flask.session.get('logged_in', False):
            flask.flash("You must log in to view this page.")
            return flask.redirect(flask.url_for('login'))
        return f(*args, **kwargs)
    return decorated
