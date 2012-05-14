from functools import wraps
from flask import Response, request
import flask
import config

def check(username, password):
    return username == config.USERNAME and password == config.PASSWORD

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not flask.session.get('logged_in', False):
            flask.flash("You must log in to view this page.")
            return flask.redirect(flask.url_for('login'))
        return f(*args, **kwargs)
    return decorated
