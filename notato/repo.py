import os
import os.path
import config
from flask.ext import shelve
from notato import app
from flask import g

@app.before_request
def before_request():
    g.db = shelve.get_shelve('c')
    g.note_ids = _get_ids()

def _get_ids():
    return sorted(map(int, g.db))

def save(note):
    g.db[str(note.id)] = note
    g.note_ids = _get_ids()

def get(note_id):
    if not str(note_id) in g.db:
        return None
    return g.db[str(note_id)]

def delete(note_id):
    del g.db[str(note_id)]
    g.note_ids = _get_ids()

def next_id():
    next_id = 1
    while next_id in g.note_ids:
        next_id += 1
    return next_id
