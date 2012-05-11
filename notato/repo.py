import os
import os.path
import config
from flask.ext import shelve
from notato import app
from flask import g

class Note:
    def __init__(self, note_id=None, title="", text=""):
        self.id = note_id
        self.title = title
        self.text = text

@app.before_request
def before_request():
    g.db = shelve.get_shelve('c')
    g.note_ids = list_ids()

def list_ids():
    return sorted(map(int, g.db))

def write(note):
    g.db[str(n.id)] = note
    g.note_ids = list_ids()

def read(note_id):
    if not str(note_id) in g.db:
        return None
    return g.db[str(note_id)]

def delete(note_id):
    del g.db[str(note_id)]
    g.note_ids = list_ids()

def next_id():
    next_id = 1
    while next_id in g.note_ids:
        next_id += 1
    return next_id
