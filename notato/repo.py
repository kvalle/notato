from notato import app
from flask import g
from bson.objectid import ObjectId
from pymongo import Connection
from notato.models import Note

class MongoRepo():

    def __init__(self):
        con = Connection()
        self.mongo = con[app.config['DATABASE']]
        
    def get_ids(self):
        return [n['note_id'] for n in self.mongo.notes.find()]

    def insert(self, note):
        _id = self.mongo.notes.insert(_as_data(note))
        return _id

    def get(self, note_id):
        d = self.mongo.notes.find_one({'note_id':note_id})
        return Note(d['note_id'], d['title'], d['text'], d['markdown'])

    def delete(self, note_id):
        self.mongo.notes.remove({'note_id':note_id})

    def clear_all(self):
        self.mongo.notes.drop()

@app.before_request
def before_request():
    g.mongo = Connection().notato
    g.repo = MongoRepo()
    g.note_ids = get_ids()

def _as_data(note):
    return {'note_id': note.id, 'title':note.title, 'text':note.text, 'markdown':note.markdown}

def get_ids():
    return g.repo.get_ids()

def insert(note):
    _id = g.repo.insert(note)
    g.note_ids.append(note.id)

def get(note_id):
    return g.repo.get(note_id)

def delete(note_id):
    g.repo.delete(note_id)
    g.note_ids.remove(note_id)

def next_id():
    if not g.note_ids:
        return 1
    return max(g.note_ids) + 1

