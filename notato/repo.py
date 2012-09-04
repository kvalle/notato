import os
import os.path
from flask.ext import shelve
from pymongo import Connection
from notato import app
from flask import g
from bson.objectid import ObjectId
from notato.models import Note

@app.before_request
def before_request():
    g.mongo = Connection().notato
    g.note_ids = _get_ids()

def _get_ids():
    return [n['note_id'] for n in g.mongo.notes.find()]

def insert(note):
    _id = g.mongo.notes.insert(_as_data(note))
    g.note_ids.append(note.id)

def get(note_id):
    d = g.mongo.notes.find_one({'note_id':note_id})
    return Note(d['note_id'], d['title'], d['text'], d['markdown'])

def delete(note_id):
    g.mongo.notes.remove({'note_id':note_id})
    g.note_ids.remove(note_id)

def _as_data(note):
    return {'note_id': note.id, 'title':note.title, 'text':note.text, 'markdown':note.markdown}

def next_id():
    next_id = 1
    while next_id in g.note_ids:
        next_id += 1
    return next_id
