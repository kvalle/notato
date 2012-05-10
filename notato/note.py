import os
import os.path
import config
from flask.ext import shelve
from notato import app
from flask import g

@app.before_request
def before_request():
    g.db = shelve.get_shelve('c')

def list_ids():
    return sorted(map(int, g.db))

def write(note_id, text):
    g.db[str(note_id)] = text
        
def read(note_id):
    if not str(note_id) in g.db:
        return ""
    return g.db[str(note_id)]

def delete(note_id):
    del g.db[str(note_id)]
