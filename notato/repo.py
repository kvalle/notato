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
        return [n['_id'] for n in self.mongo.notes.find()]
        
    def get_title_by_id(self, note_id):
        d = self.mongo.notes.find_one({'_id': note_id})
        note = Note(note_id, title=d['title'])
        return note.title_or_placeholder

    def save(self, note):
        return self.mongo.notes.save(note.as_data())

    def get(self, note_id):
        d = self.mongo.notes.find_one({'_id': note_id})
        return Note(d['_id'], d['title'], d['text'], d['markdown'])

    def delete(self, note_id):
        self.mongo.notes.remove({'_id': note_id})

    def clear_all(self):
        self.mongo.notes.drop()

@app.before_request
def before_request():
    g.repo = MongoRepo()

def next_id():
    if not g.repo.get_ids():
        return 1
    return max(g.repo.get_ids()) + 1

