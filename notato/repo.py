import os
import os.path
import config
from flask.ext import shelve
from notato import app
from flask import g

class Note:
    def __init__(self, nid=None, title="", text=""):
        self.id = nid
        self.title = title
        self.text = text

@app.before_request
def before_request():
    g.db = shelve.get_shelve('c')
    g.note_ids = list_ids()

def list_ids():
    return sorted(map(int, g.db))

def write(n):
    g.db[str(n.id)] = n
    g.note_ids = list_ids()

def is_note(note_id):
    return str(note_id) in g.db

def read(note_id):
    if not is_note(note_id):
        return ("", "")
    n = g.db[str(note_id)]
    return n

def delete(note_id):
    del g.db[str(note_id)]
    g.note_ids = list_ids()

def next_id():
    next_id = 1
    while next_id in g.note_ids:
        next_id += 1
    return next_id
