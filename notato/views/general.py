from flask import g
import flask
import markdown

import notato.auth as auth
import notato.repo as repo

from notato.auth import requires_auth
from notato.models import Note
from notato import app

@app.route('/about/')
@auth.requires_auth
def about():
    return flask.render_template('about.html')

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

